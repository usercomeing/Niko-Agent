from niko_agent import Niko, SessionStore
from niko_agent.core import runtime_checkpoints
from niko_agent.core import workspace as workspace_module
from niko_agent.core.workspace import WorkspaceContext
from niko_agent.testing import ScriptedModelClient


def test_repo_root_override_does_not_probe_parent_git(monkeypatch, tmp_path):
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "README.md").write_text("isolated\n", encoding="utf-8")
    git_calls = []

    def record_git_call(*args, **kwargs):
        git_calls.append((args, kwargs))
        raise AssertionError("an isolated non-Git fixture must not invoke Git")

    monkeypatch.setattr(workspace_module.subprocess, "run", record_git_call)

    workspace = WorkspaceContext.build(fixture, repo_root_override=fixture)

    assert git_calls == []
    assert workspace.cwd == str(fixture.resolve())
    assert workspace.repo_root == str(fixture.resolve())
    assert workspace.branch == "-"
    assert workspace.status == "clean"
    assert workspace.recent_commits == []
    assert workspace.git_available is False


def test_non_git_checkpoint_enumeration_stays_inside_isolated_root(
    monkeypatch, tmp_path
):
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    (fixture / "public.txt").write_text("public\n", encoding="utf-8")
    (fixture / ".env").write_text("SECRET=hidden\n", encoding="utf-8")
    workspace = WorkspaceContext.build(fixture, repo_root_override=fixture)
    agent = Niko(
        model_client=ScriptedModelClient([]),
        workspace=workspace,
        session_store=SessionStore(fixture / ".niko" / "sessions"),
        approval_policy="auto",
    )

    def unexpected_git(*args, **kwargs):
        raise AssertionError("non-Git isolated roots must not invoke Git")

    monkeypatch.setattr(runtime_checkpoints.subprocess, "run", unexpected_git)

    files = dict(agent.git_visible_files())
    workspace_snapshot = agent.capture_workspace_snapshot()

    assert set(files) == {"public.txt"}
    assert set(workspace_snapshot) == {"public.txt"}
