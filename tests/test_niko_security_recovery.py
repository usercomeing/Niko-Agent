import json
import subprocess
from datetime import datetime, timedelta, timezone

import pytest

from niko_agent import Niko, SessionStore, WorkspaceContext
from niko_agent.cli import handle_repl_command
from niko_agent.core import runtime_checkpoints, session_branch
from niko_agent.testing import ScriptedModelClient
from niko_agent.tools import file_tools, registry


def build_agent(tmp_path, outputs=None):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("one\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    return Niko(
        model_client=ScriptedModelClient(outputs or ["<final>checkpoint ready</final>"]),
        workspace=WorkspaceContext.build(tmp_path, repo_root_override=tmp_path),
        session_store=SessionStore(tmp_path / ".niko" / "sessions"),
        approval_policy="auto",
    )


def current_checkpoint(agent):
    return agent.session["checkpoints"]["items"][
        agent.session["checkpoints"]["current_id"]
    ]


def checkpoint_manifest(agent):
    checkpoint = current_checkpoint(agent)
    path = agent.root / checkpoint["rollback_snapshot_path"] / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "path",
    [
        ".env",
        ".ENV.production",
        ".NiKo.ToMl",
        ".niko/sessions/x.json",
        ".niko/memory/MEMORY.md",
        "SERVER.KEY",
        ".SSH/id_rsa",
        ".AWS/CREDENTIALS",
        ".Docker/CONFIG.JSON",
        ".KUBE/CONFIG",
    ],
)
def test_model_file_tools_reject_sensitive_paths(tmp_path, path):
    agent = build_agent(tmp_path)
    target = tmp_path / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("secret\n", encoding="utf-8")

    result = agent.run_tool("read_file", {"path": path, "start": 1, "end": 2})

    assert "sensitive path" in result
    assert "secret" not in result


def test_env_example_remains_available(tmp_path):
    agent = build_agent(tmp_path)
    (tmp_path / ".env.example").write_text("API_KEY=\n", encoding="utf-8")

    result = agent.run_tool("read_file", {"path": ".env.example", "start": 1, "end": 2})

    assert "API_KEY=" in result


def test_dream_profile_can_only_access_curated_memory_subtree(tmp_path):
    agent = build_agent(tmp_path)
    memory_index = tmp_path / ".niko" / "memory" / "MEMORY.md"
    memory_index.parent.mkdir(parents=True, exist_ok=True)
    memory_index.write_text("# Memory\n", encoding="utf-8")
    session_file = tmp_path / ".niko" / "sessions" / "private.json"
    session_file.write_text('{"secret": true}\n', encoding="utf-8")
    nested_secret = tmp_path / ".niko" / "memory" / ".env"
    nested_secret.write_text("TOKEN=hidden\n", encoding="utf-8")
    agent.set_tool_profile("dream")

    memory_result = agent.run_tool(
        "read_file",
        {"path": ".niko/memory/MEMORY.md", "start": 1, "end": 2},
    )
    session_result = agent.run_tool(
        "read_file",
        {"path": ".niko/sessions/private.json", "start": 1, "end": 2},
    )
    secret_result = agent.run_tool(
        "read_file", {"path": ".niko/memory/.env", "start": 1, "end": 2}
    )

    assert "# Memory" in memory_result
    assert "sensitive path" in session_result
    assert "sensitive path" in secret_result
    assert "hidden" not in secret_result


@pytest.mark.parametrize("tool_name", ["write_file", "patch_file"])
def test_model_write_tools_reject_sensitive_paths(tmp_path, tool_name):
    agent = build_agent(tmp_path)
    (tmp_path / ".env").write_text("SECRET=old\n", encoding="utf-8")
    args = {"path": ".env", "content": "SECRET=new\n"}
    if tool_name == "patch_file":
        args = {"path": ".env", "old_text": "old", "new_text": "new"}

    result = agent.run_tool(tool_name, args)

    assert "sensitive path" in result
    assert (tmp_path / ".env").read_text(encoding="utf-8") == "SECRET=old\n"


def test_list_and_search_hide_sensitive_paths_but_allow_env_template(tmp_path):
    agent = build_agent(tmp_path)
    fixtures = {
        "public.txt": "shared-marker public\n",
        ".env": "shared-marker env-secret\n",
        ".env.example": "shared-marker template\n",
        ".SSH/id_rsa": "shared-marker ssh-secret\n",
        ".AWS/credentials": "shared-marker cloud-secret\n",
        ".config/gcloud/credentials.db": "shared-marker gcloud-secret\n",
    }
    for relative, content in fixtures.items():
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    listing = agent.run_tool("list_files", {"path": "."})
    search = agent.run_tool("search", {"pattern": "shared-marker", "path": "."})

    assert ".env.example" in listing
    assert ".env\n" not in f"{listing}\n"
    assert ".SSH" not in listing
    assert "public.txt" in search
    assert ".env.example" in search
    assert "env-secret" not in search
    assert "ssh-secret" not in search
    assert "cloud-secret" not in search
    assert "gcloud-secret" not in search


def test_rg_search_receives_only_prevalidated_files(tmp_path, monkeypatch):
    agent = build_agent(tmp_path)
    (tmp_path / "public.txt").write_text("marker public\n", encoding="utf-8")
    (tmp_path / ".env").write_text("marker secret\n", encoding="utf-8")
    (tmp_path / ".env.example").write_text("marker template\n", encoding="utf-8")
    captured = []

    class Result:
        returncode = 1
        stdout = ""
        stderr = ""

    def fake_run(command, **kwargs):
        captured.extend(command)
        return Result()

    monkeypatch.setattr(file_tools.shutil, "which", lambda name: "rg")
    monkeypatch.setattr(file_tools.subprocess, "run", fake_run)

    result = registry.tool_search(agent, {"pattern": "marker", "path": "."})

    assert result == "(no matches)"
    assert "public.txt" in captured
    assert ".env.example" in captured
    assert ".env" not in captured


def test_sensitive_symlink_alias_is_rejected(tmp_path):
    agent = build_agent(tmp_path)
    (tmp_path / ".env").write_text("SECRET=hidden\n", encoding="utf-8")
    try:
        (tmp_path / "public-name.txt").symlink_to(tmp_path / ".env")
    except OSError as exc:
        pytest.skip(f"symlinks unavailable: {exc}")

    result = agent.run_tool(
        "read_file", {"path": "public-name.txt", "start": 1, "end": 2}
    )

    assert "sensitive path" in result
    assert "hidden" not in result


@pytest.mark.parametrize(
    "command",
    [
        "echo .AWS\\credentials",
        "echo .Azure\\accessTokens.json",
        "echo .config/gcloud/credentials.db",
        "echo .Docker/config.json",
        "echo .KUBE/config",
        "echo service-account-prod.json",
    ],
)
def test_shell_policy_rejects_cloud_credential_paths(tmp_path, command):
    agent = build_agent(tmp_path)

    result = agent.run_tool("run_shell", {"command": command, "timeout": 20})

    assert "sensitive paths" in result


def test_fork_keeps_workspace_and_parent_session(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed")
    parent_id = agent.session["id"]
    parent_history = list(agent.session["history"])

    result = agent.fork_session("latest")

    assert result["workspace_restored"] is False
    assert result["parent_session_id"] == parent_id
    assert agent.session["id"] != parent_id
    assert agent.session_store.load(parent_id)["history"] == parent_history
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "one\n"


@pytest.mark.parametrize(
    ("target_kind", "expected_history_count"),
    [("index", 1), ("event_id", 1), ("turn_id", 2)],
)
def test_fork_accepts_index_event_id_and_turn_id(
    tmp_path, target_kind, expected_history_count
):
    agent = build_agent(tmp_path)
    agent.ask("seed")
    parent_id = agent.session["id"]
    parent_history = list(agent.session["history"])
    first = parent_history[0]
    target = {
        "index": "1",
        "event_id": first["event_id"],
        "turn_id": first["turn_id"],
    }[target_kind]

    result = agent.fork_session(target)

    assert len(agent.session["history"]) == expected_history_count
    assert agent.session_store.load(parent_id)["history"] == parent_history
    assert result["event_id"] == agent.session["history"][-1]["event_id"]


@pytest.mark.parametrize(
    "command", ["/rollback --confirm", "/rollback --confirm token extra"]
)
def test_rollback_confirm_requires_exactly_one_token(tmp_path, command):
    agent = build_agent(tmp_path)

    handled, should_exit, output = handle_repl_command(agent, command)

    assert handled is True
    assert should_exit is False
    assert output == "Usage: /rollback --confirm <token>"


def test_rollback_requires_preview_and_restores_git_visible_workspace(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    parent_id = agent.session["id"]
    parent_history = list(agent.session["history"])
    (tmp_path / "README.md").write_text("two\n", encoding="utf-8")
    (tmp_path / "later.txt").write_text("later\n", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=do-not-touch\n", encoding="utf-8")

    preview = agent.preview_rollback("latest")

    assert "README.md" in preview["modified"]
    assert "later.txt" in preview["deleted"]
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "two\n"

    result = agent.confirm_rollback(preview["token"])

    assert result["workspace_restored"] is True
    assert result["parent_session_id"] == parent_id
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "one\n"
    assert not (tmp_path / "later.txt").exists()
    assert (tmp_path / ".env").read_text(encoding="utf-8") == "TOKEN=do-not-touch\n"
    assert agent.session_store.load(parent_id)["history"] == parent_history
    assert result["status"] == "completed"
    assert result["checkpoint_manifest_sha256"]
    assert result["pre_rollback_manifest_sha256"]
    assert "sensitive paths and credentials" in result["excluded"]
    assert agent.session["branch"]["operation_id"] == result["operation_id"]
    recovery_root = tmp_path / result["recovery_path"]
    journal = json.loads(
        (recovery_root / "journal.json").read_text(encoding="utf-8")
    )
    recovery_manifest = json.loads(
        (recovery_root / "manifest.json").read_text(encoding="utf-8")
    )
    recovery_report = json.loads(
        (recovery_root / "report.json").read_text(encoding="utf-8")
    )
    assert journal["status"] == "completed"
    assert journal["child_session_id"] == agent.session["id"]
    assert recovery_report["status"] == "completed"
    assert recovery_report["child_session_id"] == agent.session["id"]
    assert "token" not in recovery_manifest["preview"]
    assert preview["token"] not in json.dumps(recovery_report)
    parent_events_path = agent.session_store.event_path(parent_id)
    parent_events = [
        json.loads(line)
        for line in parent_events_path.read_text(encoding="utf-8").splitlines()
    ]
    assert any(
        event["event"] == "rollback_confirmation_started"
        for event in parent_events
    )
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_rollback_refuses_when_workspace_changes_after_preview(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    preview = agent.preview_rollback("latest")
    (tmp_path / "new.txt").write_text("changed after preview\n", encoding="utf-8")

    with pytest.raises(ValueError, match="workspace changed"):
        agent.confirm_rollback(preview["token"])

    (tmp_path / "new.txt").unlink()
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_rollback_token_expires_and_cannot_be_reused(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    preview = agent.preview_rollback("latest")
    preview["expires_at"] = (
        datetime.now(timezone.utc) - timedelta(seconds=1)
    ).isoformat()

    with pytest.raises(ValueError, match="expired"):
        agent.confirm_rollback(preview["token"])
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_oversized_snapshot_is_unavailable_instead_of_partial(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(runtime_checkpoints, "MAX_SNAPSHOT_FILE_BYTES", 3)
    agent = build_agent(tmp_path)

    agent.ask("seed oversized checkpoint")

    checkpoint = current_checkpoint(agent)
    assert checkpoint["rollback_snapshot_available"] is False
    assert checkpoint["rollback_file_count"] == 0
    assert "exceeds 16 MiB" in checkpoint["rollback_unavailable_reason"]
    with pytest.raises(ValueError, match="no complete rollback snapshot"):
        agent.preview_rollback("latest")


def test_total_snapshot_limit_is_unavailable_instead_of_partial(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(runtime_checkpoints, "MAX_SNAPSHOT_TOTAL_BYTES", 5)
    agent = build_agent(tmp_path)
    (tmp_path / "second.txt").write_text("two\n", encoding="utf-8")

    agent.ask("seed oversized total checkpoint")

    checkpoint = current_checkpoint(agent)
    assert checkpoint["rollback_snapshot_available"] is False
    assert checkpoint["rollback_file_count"] == 0
    assert "exceeds 128 MiB" in checkpoint["rollback_unavailable_reason"]


def test_snapshot_excludes_sensitive_files_and_symbolic_links(tmp_path):
    agent = build_agent(tmp_path)
    (tmp_path / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("ignored\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore"], cwd=tmp_path, check=True)
    sensitive_paths = [".env", "SERVER.KEY", ".SSH/id_rsa"]
    for relative in sensitive_paths:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("secret\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "-f", *sensitive_paths], cwd=tmp_path, check=True
    )
    link = tmp_path / "readme-link.txt"
    try:
        link.symlink_to(tmp_path / "README.md")
    except OSError:
        pytest.skip("symbolic links are unavailable on this Windows host")
    subprocess.run(["git", "add", "readme-link.txt"], cwd=tmp_path, check=True)

    agent.ask("capture filtered checkpoint")

    files = checkpoint_manifest(agent)["files"]
    assert "README.md" in files
    assert ".gitignore" in files
    assert "ignored.txt" not in files
    assert "readme-link.txt" not in files
    assert not any(path.casefold() in {item.casefold() for item in files} for path in sensitive_paths)
    assert current_checkpoint(agent)["excluded"] == list(
        runtime_checkpoints.SNAPSHOT_EXCLUSIONS
    )


def test_rollback_rejects_corrupted_snapshot_and_consumes_token(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    checkpoint = current_checkpoint(agent)
    snapshot_file = (
        tmp_path / checkpoint["rollback_snapshot_path"] / "files" / "README.md"
    )
    snapshot_file.write_text("tampered\n", encoding="utf-8")
    preview = agent.preview_rollback("latest")

    with pytest.raises(ValueError, match="hash mismatch"):
        agent.confirm_rollback(preview["token"])
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_windows_manifest_path_collision_is_rejected():
    manifest = {
        "Source/Readme.md": {"sha256": "a", "size": 1},
        "source/README.md": {"sha256": "b", "size": 1},
    }

    with pytest.raises(ValueError, match="path collision"):
        session_branch._manifest_path_map(manifest, case_insensitive=True)


@pytest.mark.parametrize(
    "path",
    ["../README.md", "nested/../README.md", "nested//README.md", "/README.md"],
)
def test_noncanonical_manifest_paths_are_rejected(path):
    with pytest.raises(ValueError, match="non-canonical rollback path"):
        session_branch._manifest_path_map(
            {path: {"sha256": "a", "size": 1}}, case_insensitive=False
        )


def test_rollback_interruption_restores_pre_operation_workspace(
    tmp_path, monkeypatch
):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    parent_id = agent.session["id"]
    parent_history = list(agent.session["history"])
    (tmp_path / "README.md").write_text("two\n", encoding="utf-8")
    (tmp_path / "later.txt").write_text("later\n", encoding="utf-8")
    preview = agent.preview_rollback("latest")
    original_restore = session_branch._restore_manifest
    calls = []

    def interrupt_first_restore(runtime, source_root, desired):
        calls.append(str(source_root))
        if len(calls) == 1:
            (runtime.root / "README.md").write_text(
                "partially restored\n", encoding="utf-8"
            )
            raise OSError("simulated restore interruption")
        return original_restore(runtime, source_root, desired)

    monkeypatch.setattr(
        session_branch, "_restore_manifest", interrupt_first_restore
    )

    with pytest.raises(ValueError, match="original workspace restored"):
        agent.confirm_rollback(preview["token"])

    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "two\n"
    assert (tmp_path / "later.txt").read_text(encoding="utf-8") == "later\n"
    assert agent.session["id"] == parent_id
    assert agent.session_store.load(parent_id)["history"] == parent_history
    recovery_roots = list((tmp_path / ".niko" / "recovery").iterdir())
    assert len(recovery_roots) == 1
    journal = json.loads(
        (recovery_roots[0] / "journal.json").read_text(encoding="utf-8")
    )
    report = json.loads(
        (recovery_roots[0] / "report.json").read_text(encoding="utf-8")
    )
    assert journal["status"] == "recovered_after_failure"
    assert report["status"] == "recovered_after_failure"
    assert report["workspace_recovered"] is True
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_rollback_backup_failure_does_not_modify_workspace(tmp_path, monkeypatch):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    parent_id = agent.session["id"]
    (tmp_path / "README.md").write_text("two\n", encoding="utf-8")
    preview = agent.preview_rollback("latest")

    def fail_backup(*args, **kwargs):
        raise OSError("simulated backup failure")

    monkeypatch.setattr(session_branch, "_copy_manifest_files", fail_backup)

    with pytest.raises(ValueError, match="backup failed before workspace modification"):
        agent.confirm_rollback(preview["token"])

    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "two\n"
    assert agent.session["id"] == parent_id
    recovery_roots = list((tmp_path / ".niko" / "recovery").iterdir())
    assert len(recovery_roots) == 1
    journal = json.loads(
        (recovery_roots[0] / "journal.json").read_text(encoding="utf-8")
    )
    report = json.loads(
        (recovery_roots[0] / "report.json").read_text(encoding="utf-8")
    )
    assert journal["status"] == "backup_failed"
    assert report["status"] == "backup_failed"
    assert report["workspace_recovered"] is True
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_failure_after_child_creation_marks_child_failed_and_restores_parent(
    tmp_path, monkeypatch
):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    parent_id = agent.session["id"]
    (tmp_path / "README.md").write_text("two\n", encoding="utf-8")
    preview = agent.preview_rollback("latest")
    original_write_json = session_branch._write_json

    def fail_completed_journal(path, payload):
        if path.name == "journal.json" and payload.get("status") == "completed":
            raise OSError("simulated completed-journal failure")
        return original_write_json(path, payload)

    monkeypatch.setattr(session_branch, "_write_json", fail_completed_journal)

    with pytest.raises(ValueError, match="original workspace restored"):
        agent.confirm_rollback(preview["token"])

    assert agent.session["id"] == parent_id
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "two\n"
    child_sessions = [
        row for row in agent.session_store.list_sessions() if row["id"] != parent_id
    ]
    assert len(child_sessions) == 1
    failed_child = agent.session_store.load(child_sessions[0]["id"])
    assert failed_child["branch"]["status"] == "rollback_failed"
    assert failed_child["branch"]["workspace_restored"] is False
    recovery_root = next((tmp_path / ".niko" / "recovery").iterdir())
    journal = json.loads(
        (recovery_root / "journal.json").read_text(encoding="utf-8")
    )
    assert journal["status"] == "recovered_after_failure"
    assert journal["failed_child_session_id"] == failed_child["id"]

