"""Append-only session forks and token-confirmed workspace rollback."""

from __future__ import annotations

import copy
import json
import os
import secrets
import shutil
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


def _copy_manifest_files(source_root, manifest, target_root):
    for relative in manifest:
        if is_sensitive_path(relative):
            raise SessionBranchError(f"sensitive path in rollback manifest: {relative}")
        source = source_root / Path(relative)
        target = target_root / Path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def _restore_manifest(runtime, source_root, desired):
    current = runtime.workspace_content_manifest()
    for relative in sorted(set(current) - set(desired), reverse=True):
        path = runtime.root / Path(relative)
        if path.exists() and path.is_file() and not path.is_symlink():
            path.unlink()
    for relative in sorted(desired):
        source = source_root / Path(relative)
        target = runtime.root / Path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(f".{target.name}.{uuid.uuid4().hex}.rollback")
        shutil.copyfile(source, temp)
        os.replace(temp, target)


def confirm_runtime_rollback(runtime, token):
    previews = runtime.session.setdefault("rollback_previews", {})
    preview = previews.get(str(token))
    if not preview:
        raise SessionBranchError("rollback token is invalid or already used")
    if datetime.now(timezone.utc) >= datetime.fromisoformat(preview["expires_at"]):
        previews.pop(str(token), None)
        runtime.session_store.save(runtime.session)
        raise SessionBranchError("rollback token expired")
    current = runtime.workspace_content_manifest()
    if runtime.manifest_fingerprint(current) != preview["workspace_fingerprint"]:
        raise SessionBranchError("workspace changed after preview; generate a new rollback preview")

    parent = copy.deepcopy(runtime.session)
    checkpoint = runtime.session["checkpoints"]["items"][preview["checkpoint_id"]]
    snapshot_root = runtime.root / checkpoint["rollback_snapshot_path"]
    desired = json.loads((snapshot_root / "manifest.json").read_text(encoding="utf-8"))["files"]
    operation_id = "rollback_" + uuid.uuid4().hex[:10]
    recovery_root = runtime.root / ".niko" / "recovery" / operation_id
    recovery_files = recovery_root / "files"
    recovery_files.mkdir(parents=True, exist_ok=True)
    _copy_manifest_files(runtime.root, current, recovery_files)
    (recovery_root / "manifest.json").write_text(
        json.dumps({"files": current, "preview": preview}, indent=2, sort_keys=True), encoding="utf-8"
    )
    try:
        _restore_manifest(runtime, snapshot_root / "files", desired)
    except Exception:
        _restore_manifest(runtime, recovery_files, current)
        raise
    previews.pop(str(token), None)
    result = _child_session(runtime, parent, int(preview["target_index"]), "rollback", checkpoint)
    result["operation_id"] = operation_id
    result["created"] = preview["created"]
    result["modified"] = preview["modified"]
    result["deleted"] = preview["deleted"]
    runtime.session_event_bus.emit("rollback_completed", result)
    runtime.session_store.save(runtime.session)
    return result

