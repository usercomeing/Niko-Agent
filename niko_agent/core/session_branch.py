"""Append-only session forks and token-confirmed workspace rollback."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import posixpath
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .session_lifecycle import _rebind, _shutdown_workers
from .sensitive_paths import is_sensitive_path
from .workspace import now


class SessionBranchError(ValueError):
    pass


def _history_index(history, target):
    value = str(target or "latest").strip()
    if value in {"", "latest"}:
        return len(history) - 1
    if value.isdigit() and 0 < int(value) <= len(history):
        return int(value) - 1
    for index, item in enumerate(history):
        if value == str(item.get("event_id", "")):
            return index
    matches = [index for index, item in enumerate(history) if value == str(item.get("turn_id", ""))]
    if matches:
        return matches[-1]
    raise SessionBranchError(f"history point not found: {value}")


def _checkpoint_for_index(session, index):
    items = (session.get("checkpoints", {}) or {}).get("items", {}) or {}
    candidates = [
        item for item in items.values()
        if int(item.get("history_count", 0)) <= index + 1
        and item.get("rollback_snapshot_available")
    ]
    if not candidates:
        raise SessionBranchError("selected point has no complete rollback snapshot")
    return sorted(candidates, key=lambda item: (int(item.get("history_count", 0)), item.get("created_at", "")))[-1]


def _child_session(runtime, parent, index, mode, checkpoint=None):
    history = list(parent.get("history", []))
    child = copy.deepcopy(parent)
    child_id = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{mode}-" + uuid.uuid4().hex[:6]
    child["id"] = child_id
    child["created_at"] = now()
    child["history"] = copy.deepcopy(history[: index + 1])
    child["parent_session_id"] = parent.get("id", "")
    child["branch"] = {
        "mode": mode,
        "parent_session_id": parent.get("id", ""),
        "event_id": history[index].get("event_id", ""),
        "turn_id": history[index].get("turn_id", ""),
        "checkpoint_id": (checkpoint or {}).get("checkpoint_id", ""),
        "workspace_restored": mode == "rollback",
        "created_at": child["created_at"],
    }
    child["workers"] = {"items": []}
    child["todos"] = {"items": []}
    child["runtime_mode"] = {"mode": "default"}
    child.pop("rollback_previews", None)
    if checkpoint:
        child.setdefault("checkpoints", {})["current_id"] = checkpoint["checkpoint_id"]
    _shutdown_workers(runtime)
    runtime.session = child
    _rebind(runtime, emit_started=True)
    runtime.session_event_bus.emit("session_branch_created", child["branch"])
    runtime.session_path = runtime.session_store.save(runtime.session)
    return dict(child["branch"], session_id=child_id)


def fork_runtime_session(runtime, target="latest"):
    parent = copy.deepcopy(runtime.session)
    history = list(parent.get("history", []))
    if not history:
        raise SessionBranchError("current session has no history")
    return _child_session(runtime, parent, _history_index(history, target), "fork")


def preview_runtime_rollback(runtime, target="latest"):
    history = list(runtime.session.get("history", []))
    if not history:
        raise SessionBranchError("current session has no history")
    index = _history_index(history, target)
    checkpoint = _checkpoint_for_index(runtime.session, index)
    snapshot_root = runtime.root / checkpoint["rollback_snapshot_path"]
    payload = json.loads((snapshot_root / "manifest.json").read_text(encoding="utf-8"))
    desired = payload["files"]
    current = runtime.workspace_content_manifest()
    created = sorted(set(desired) - set(current))
    deleted = sorted(set(current) - set(desired))
    modified = sorted(path for path in set(current) & set(desired) if current[path] != desired[path])
    token = secrets.token_urlsafe(18)
    expires = datetime.now(timezone.utc) + timedelta(minutes=10)
    preview = {
        "token": token,
        "target_index": index,
        "checkpoint_id": checkpoint["checkpoint_id"],
        "workspace_fingerprint": runtime.manifest_fingerprint(current),
        "expires_at": expires.isoformat(),
        "created": created,
        "modified": modified,
        "deleted": deleted,
    }
    runtime.session.setdefault("rollback_previews", {})[token] = preview
    runtime.session_path = runtime.session_store.save(runtime.session)
    runtime.session_event_bus.emit(
        "rollback_preview_created",
        {key: value for key, value in preview.items() if key != "token"},
    )
    return preview


def _normalized_manifest_path(relative):
    relative = str(relative).replace("\\", "/")
    normalized = posixpath.normpath(relative)
    if (
        relative in {"", ".", ".."}
        or relative.startswith("/")
        or normalized != relative
        or normalized.startswith("../")
    ):
        raise SessionBranchError(f"non-canonical rollback path: {relative}")
    return normalized


def _safe_manifest_path(root, relative, *, reject_symlink=False):
    relative = _normalized_manifest_path(relative)
    if is_sensitive_path(relative):
        raise SessionBranchError(f"sensitive path in rollback manifest: {relative}")
    root = Path(root).resolve()
    candidate = root / Path(relative)
    if reject_symlink and candidate.is_symlink():
        raise SessionBranchError(f"symbolic link in rollback manifest: {relative}")
    path = candidate.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise SessionBranchError(f"path escapes rollback root: {relative}") from exc
    return path


def _manifest_path_map(manifest, *, case_insensitive=None):
    if not isinstance(manifest, dict):
        raise SessionBranchError("rollback manifest files must be a mapping")
    if case_insensitive is None:
        case_insensitive = os.name == "nt"
    mapped = {}
    for relative in manifest:
        normalized = _normalized_manifest_path(relative)
        key = normalized.casefold() if case_insensitive else normalized
        if key in mapped:
            raise SessionBranchError(
                f"rollback manifest contains a path collision: {normalized}"
            )
        mapped[key] = normalized
    return mapped


def _validated_manifest_bytes(source_root, manifest):
    _manifest_path_map(manifest)
    contents = {}
    for relative, metadata in manifest.items():
        relative = _normalized_manifest_path(relative)
        if not isinstance(metadata, dict):
            raise SessionBranchError(f"invalid rollback metadata: {relative}")
        source = _safe_manifest_path(source_root, relative, reject_symlink=True)
        if not source.is_file():
            raise SessionBranchError(f"rollback source is unavailable: {relative}")
        data = source.read_bytes()
        expected_size = int(metadata.get("size", -1))
        expected_sha256 = str(metadata.get("sha256", ""))
        actual_sha256 = hashlib.sha256(data).hexdigest()
        if len(data) != expected_size or actual_sha256 != expected_sha256:
            raise SessionBranchError(f"rollback source hash mismatch: {relative}")
        contents[relative] = data
    return contents


def _copy_manifest_files(source_root, manifest, target_root):
    contents = _validated_manifest_bytes(source_root, manifest)
    for relative, data in contents.items():
        target = _safe_manifest_path(target_root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def _restore_manifest(runtime, source_root, desired):
    contents = _validated_manifest_bytes(source_root, desired)
    current = runtime.workspace_content_manifest()
    current_paths = _manifest_path_map(current)
    desired_paths = _manifest_path_map(desired)
    delete_paths = [
        relative
        for key, relative in current_paths.items()
        if key not in desired_paths or desired_paths[key] != relative
    ]
    for relative in sorted(delete_paths, reverse=True):
        path = _safe_manifest_path(runtime.root, relative)
        if path.exists() and path.is_file() and not path.is_symlink():
            path.unlink()
    for relative in sorted(contents):
        target = _safe_manifest_path(runtime.root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(f".{target.name}.{uuid.uuid4().hex}.rollback")
        temp.write_bytes(contents[relative])
        os.replace(temp, target)


def _write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temp, path)


def _record_rollback_failure(
    runtime,
    recovery_root,
    journal,
    *,
    status,
    error,
    workspace_recovered,
    recovery_error=None,
):
    journal["status"] = status
    journal["failed_at"] = now()
    journal["restore_error"] = str(error)[:500]
    journal["recovery_error"] = str(recovery_error)[:500] if recovery_error else ""
    journal_recorded = True
    try:
        _write_json(
            recovery_root / "journal.json", runtime.redact_artifact(journal)
        )
    except Exception:
        journal_recorded = False
    payload = {
        "operation_id": journal["operation_id"],
        "status": journal["status"],
        "recovery_path": str(recovery_root.relative_to(runtime.root)).replace("\\", "/"),
        "workspace_recovered": workspace_recovered,
        "journal_recorded": journal_recorded,
    }
    report_recorded = True
    try:
        _write_json(
            recovery_root / "report.json",
            runtime.redact_artifact(
                {
                    **journal,
                    "workspace_recovered": workspace_recovered,
                    "journal_recorded": journal_recorded,
                }
            ),
        )
    except Exception:
        report_recorded = False
    payload["report_recorded"] = report_recorded
    try:
        runtime.session_event_bus.emit("rollback_failed", payload)
    except Exception:
        pass
    return payload


def confirm_runtime_rollback(runtime, token):
    previews = runtime.session.setdefault("rollback_previews", {})
    preview = previews.pop(str(token), None)
    if not preview:
        raise SessionBranchError("rollback token is invalid or already used")
    runtime.session_path = runtime.session_store.save(runtime.session)
    if datetime.now(timezone.utc) >= datetime.fromisoformat(preview["expires_at"]):
        raise SessionBranchError("rollback token expired")
    current = runtime.workspace_content_manifest()
    if runtime.manifest_fingerprint(current) != preview["workspace_fingerprint"]:
        raise SessionBranchError("workspace changed after preview; generate a new rollback preview")

    parent = copy.deepcopy(runtime.session)
    checkpoint = runtime.session["checkpoints"]["items"][preview["checkpoint_id"]]
    snapshot_root = runtime.root / checkpoint["rollback_snapshot_path"]
    desired = json.loads((snapshot_root / "manifest.json").read_text(encoding="utf-8"))["files"]
    desired_fingerprint = runtime.manifest_fingerprint(desired)
    expected_fingerprint = str(checkpoint.get("rollback_manifest_sha256", ""))
    if not expected_fingerprint or desired_fingerprint != expected_fingerprint:
        raise SessionBranchError("rollback snapshot manifest hash mismatch")
    _validated_manifest_bytes(snapshot_root / "files", desired)
    operation_id = "rollback_" + uuid.uuid4().hex[:10]
    recovery_root = runtime.root / ".niko" / "recovery" / operation_id
    recovery_files = recovery_root / "files"
    recovery_files.mkdir(parents=True, exist_ok=True)
    current_fingerprint = runtime.manifest_fingerprint(current)
    sanitized_preview = {key: value for key, value in preview.items() if key != "token"}
    journal = {
        "operation_id": operation_id,
        "created_at": now(),
        "status": "backing_up",
        "parent_session_id": parent.get("id", ""),
        "checkpoint_id": checkpoint["checkpoint_id"],
        "target_index": int(preview["target_index"]),
        "pre_rollback_manifest_sha256": current_fingerprint,
        "checkpoint_manifest_sha256": desired_fingerprint,
        "excluded": list(checkpoint.get("excluded", [])),
    }
    _write_json(recovery_root / "journal.json", journal)
    try:
        runtime.session_event_bus.emit(
            "rollback_confirmation_started",
            {
                "operation_id": operation_id,
                "checkpoint_id": checkpoint["checkpoint_id"],
                "target_index": int(preview["target_index"]),
                "recovery_path": str(recovery_root.relative_to(runtime.root)).replace(
                    "\\", "/"
                ),
            },
        )
        _copy_manifest_files(runtime.root, current, recovery_files)
        _write_json(
            recovery_root / "manifest.json",
            {
                "files": current,
                "preview": sanitized_preview,
                "manifest_sha256": current_fingerprint,
            },
        )
        journal["status"] = "restoring"
        journal["backup_completed_at"] = now()
        _write_json(recovery_root / "journal.json", journal)
    except Exception as error:
        failure = _record_rollback_failure(
            runtime,
            recovery_root,
            journal,
            status="backup_failed",
            error=error,
            workspace_recovered=True,
        )
        raise SessionBranchError(
            f"rollback backup failed before workspace modification; inspect {failure['recovery_path']}"
        ) from error
    try:
        _restore_manifest(runtime, snapshot_root / "files", desired)
        result = _child_session(
            runtime,
            parent,
            int(preview["target_index"]),
            "rollback",
            checkpoint,
        )
        audit = {
            "operation_id": operation_id,
            "status": "completed",
            "created": preview["created"],
            "modified": preview["modified"],
            "deleted": preview["deleted"],
            "checkpoint_manifest_sha256": desired_fingerprint,
            "pre_rollback_manifest_sha256": current_fingerprint,
            "excluded": list(checkpoint.get("excluded", [])),
            "recovery_path": str(recovery_root.relative_to(runtime.root)).replace(
                "\\", "/"
            ),
        }
        result.update(audit)
        runtime.session["branch"].update(audit)
        journal["status"] = "completed"
        journal["completed_at"] = now()
        journal["child_session_id"] = result["session_id"]
        _write_json(recovery_root / "journal.json", journal)
        _write_json(
            recovery_root / "report.json",
            runtime.redact_artifact(
                {
                    **audit,
                    "parent_session_id": parent.get("id", ""),
                    "child_session_id": result["session_id"],
                    "checkpoint_id": checkpoint["checkpoint_id"],
                    "completed_at": journal["completed_at"],
                }
            ),
        )
        runtime.session_path = runtime.session_store.save(runtime.session)
        runtime.session_event_bus.emit("rollback_completed", result)
    except Exception as error:
        recovery_error = None
        try:
            _restore_manifest(runtime, recovery_files, current)
        except Exception as exc:
            recovery_error = exc
        failed_child_session_id = ""
        if runtime.session.get("id") != parent.get("id"):
            failed_child = copy.deepcopy(runtime.session)
            failed_child_session_id = str(failed_child.get("id", ""))
            failed_child.setdefault("branch", {}).update(
                {
                    "status": "rollback_failed",
                    "workspace_restored": False,
                    "operation_id": operation_id,
                    "failed_at": now(),
                }
            )
            try:
                runtime.session_store.save(failed_child)
            except Exception as exc:
                if recovery_error is None:
                    recovery_error = exc
        try:
            runtime.session = copy.deepcopy(parent)
            _rebind(runtime, emit_started=False)
        except Exception as exc:
            if recovery_error is None:
                recovery_error = exc
        if failed_child_session_id:
            journal["failed_child_session_id"] = failed_child_session_id
        status = (
            "recovery_failed"
            if recovery_error is not None
            else "recovered_after_failure"
        )
        failure = _record_rollback_failure(
            runtime,
            recovery_root,
            journal,
            status=status,
            error=error,
            workspace_recovered=recovery_error is None,
            recovery_error=recovery_error,
        )
        if recovery_error is not None:
            raise SessionBranchError(
                f"rollback and automatic recovery failed; inspect {failure['recovery_path']}"
            ) from recovery_error
        raise SessionBranchError(
            f"rollback failed; original workspace restored; inspect {failure['recovery_path']}"
        ) from error
    return result
