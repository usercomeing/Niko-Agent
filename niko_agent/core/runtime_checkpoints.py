"""Runtime workspace snapshot and checkpoint helpers."""

import hashlib
import json
import shutil
import subprocess
import uuid
from pathlib import Path

from ..features import memory as memorylib
from .workspace import IGNORED_PATH_NAMES, clip, now
from .sensitive_paths import is_sensitive_path

CHECKPOINT_SCHEMA_VERSION = "niko-v1"
MAX_SNAPSHOT_FILE_BYTES = 16 * 1024 * 1024
MAX_SNAPSHOT_TOTAL_BYTES = 128 * 1024 * 1024


class RuntimeCheckpointsMixin:
    def git_visible_files(self):
        """Return tracked and non-ignored untracked regular files."""
        try:
            result = subprocess.run(
                ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                cwd=self.root,
                capture_output=True,
                check=True,
                timeout=15,
            )
            candidates = [item for item in result.stdout.decode("utf-8", "replace").split("\0") if item]
        except Exception:
            candidates = [
                path.relative_to(self.root).as_posix()
                for path in self.root.rglob("*")
                if path.is_file()
                and not any(part in IGNORED_PATH_NAMES for part in path.relative_to(self.root).parts)
            ]
        files = []
        for relative in sorted(set(candidates)):
            if is_sensitive_path(relative):
                continue
            path = self.root / relative
            try:
                if path.is_symlink() or not path.is_file():
                    continue
                path.resolve().relative_to(self.root.resolve())
            except (OSError, ValueError):
                continue
            files.append((relative.replace("\\", "/"), path))
        return files

    def workspace_content_manifest(self):
        manifest = {}
        for relative, path in self.git_visible_files():
            data = path.read_bytes()
            manifest[relative] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
        return manifest

    @staticmethod
    def manifest_fingerprint(manifest):
        payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def capture_rollback_snapshot(self, checkpoint_id):
        root = self.root / ".niko" / "checkpoints" / checkpoint_id
        files_root = root / "files"
        shutil.rmtree(root, ignore_errors=True)
        files_root.mkdir(parents=True, exist_ok=True)
        manifest = {}
        total = 0
        try:
            for relative, path in self.git_visible_files():
                size = path.stat().st_size
                if size > MAX_SNAPSHOT_FILE_BYTES:
                    raise ValueError(f"snapshot file exceeds 16 MiB: {relative}")
                total += size
                if total > MAX_SNAPSHOT_TOTAL_BYTES:
                    raise ValueError("snapshot exceeds 128 MiB")
                data = path.read_bytes()
                target = files_root / Path(relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                manifest[relative] = {
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                }
            payload = {
                "checkpoint_id": checkpoint_id,
                "created_at": now(),
                "file_count": len(manifest),
                "total_bytes": total,
                "files": manifest,
            }
            (root / "manifest.json").write_text(
                json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
            )
            return {
                "rollback_snapshot_available": True,
                "rollback_snapshot_path": str(root.relative_to(self.root)).replace("\\", "/"),
                "rollback_file_count": len(manifest),
                "rollback_total_bytes": total,
                "rollback_manifest_sha256": self.manifest_fingerprint(manifest),
                "rollback_unavailable_reason": "",
            }
        except Exception as exc:
            shutil.rmtree(root, ignore_errors=True)
            return {
                "rollback_snapshot_available": False,
                "rollback_snapshot_path": "",
                "rollback_file_count": 0,
                "rollback_total_bytes": 0,
                "rollback_manifest_sha256": "",
                "rollback_unavailable_reason": str(exc),
            }

    def capture_workspace_snapshot(self):
        snapshot = {}
        for path in self.root.rglob("*"):
            try:
                relative_parts = path.relative_to(self.root).parts
            except ValueError:
                continue
            if any(part in IGNORED_PATH_NAMES for part in relative_parts) or not path.is_file():
                continue
            try:
                snapshot[path.relative_to(self.root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            except Exception:
                continue
        return snapshot

    @staticmethod
    def diff_workspace_snapshots(before, after):
        changed_paths = []
        summaries = []
        for path in sorted(set(before) | set(after)):
            if before.get(path) == after.get(path):
                continue
            changed_paths.append(path)
            if path not in before:
                summaries.append(f"created:{path}")
            elif path not in after:
                summaries.append(f"deleted:{path}")
            else:
                summaries.append(f"modified:{path}")
        return changed_paths, summaries

    def create_checkpoint(self, task_state, user_message, trigger):
        state = self.checkpoint_state()
        current = self.current_checkpoint()
        checkpoint_id = "ckpt_" + uuid.uuid4().hex[:8]
        key_files = []
        freshness = {}
        for path in self.memory.to_dict()["working"]["recent_files"]:
            file_freshness = memorylib.file_freshness(path, self.root)
            freshness[path] = file_freshness
            key_files.append({"path": path, "freshness": file_freshness})
        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "parent_checkpoint_id": current.get("checkpoint_id", "") if current else "",
            "schema_version": CHECKPOINT_SCHEMA_VERSION,
            "created_at": now(),
            "current_goal": str(user_message),
            "completed": [task_state.final_answer] if task_state.final_answer else [],
            "excluded": [],
            "current_blocker": "" if str(task_state.stop_reason or "") in ("", "final_answer_returned") else str(task_state.stop_reason),
            "next_step": self.infer_next_step(task_state),
            "key_files": key_files,
            "freshness": freshness,
            "summary": f"{trigger}: {clip(str(user_message), 120)}",
            "runtime_identity": self.current_runtime_identity(),
            "history_count": len(self.session.get("history", [])),
        }
        checkpoint.update(self.capture_rollback_snapshot(checkpoint_id))
        state["items"][checkpoint_id] = checkpoint
        state["current_id"] = checkpoint_id
        task_state.checkpoint_id = checkpoint_id
        self.session["runtime_identity"] = checkpoint["runtime_identity"]
        self.session_path = self.session_store.save(self.session)
        return checkpoint
