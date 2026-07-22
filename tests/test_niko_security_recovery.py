import subprocess

import pytest

from niko_agent import Niko, SessionStore, WorkspaceContext
from niko_agent.testing import ScriptedModelClient


def build_agent(tmp_path, outputs=None):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("one\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    return Niko(
        model_client=ScriptedModelClient(outputs or ["<final>checkpoint ready</final>"]),
        workspace=WorkspaceContext.build(tmp_path),
        session_store=SessionStore(tmp_path / ".niko" / "sessions"),
        approval_policy="auto",
    )


@pytest.mark.parametrize(
    "path",
    [".env", ".env.production", ".niko.toml", ".niko/sessions/x.json", "server.key"],
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


def test_rollback_requires_preview_and_restores_git_visible_workspace(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    parent_id = agent.session["id"]
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
    with pytest.raises(ValueError, match="invalid or already used"):
        agent.confirm_rollback(preview["token"])


def test_rollback_refuses_when_workspace_changes_after_preview(tmp_path):
    agent = build_agent(tmp_path)
    agent.ask("seed checkpoint")
    preview = agent.preview_rollback("latest")
    (tmp_path / "new.txt").write_text("changed after preview\n", encoding="utf-8")

    with pytest.raises(ValueError, match="workspace changed"):
        agent.confirm_rollback(preview["token"])

