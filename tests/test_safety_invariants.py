import json
import os
import shlex
import subprocess
import sys
from unittest.mock import patch

import pytest

from niko_agent.testing import ScriptedModelClient
from niko_agent import Niko, SessionStore, WorkspaceContext
from niko_agent import cli as niko_agent_cli
from niko_agent.core.task_state import TaskState


def build_workspace(tmp_path):
    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    return WorkspaceContext.build(tmp_path, repo_root_override=tmp_path)


def python_command(script):
    argv = [sys.executable, "-c", script]
    if os.name == "nt":
        return subprocess.list2cmdline(argv)
    return shlex.join(argv)


def build_agent(tmp_path, outputs, **kwargs):
    workspace = build_workspace(tmp_path)
    store = SessionStore(tmp_path / ".niko" / "sessions")
    approval_policy = kwargs.pop("approval_policy", "auto")
    return Niko(
        model_client=ScriptedModelClient(outputs),
        workspace=workspace,
        session_store=store,
        approval_policy=approval_policy,
        **kwargs,
    )


def test_workspace_escape_is_rejected(tmp_path):
    (tmp_path / "outside.txt").write_text("outside\n", encoding="utf-8")
    agent = build_agent(tmp_path, [])

    result = agent.run_tool("read_file", {"path": "../outside.txt"})

    assert "path escapes workspace" in result


def test_symlink_path_traversal_is_rejected(tmp_path):
    outside = tmp_path.parent / f"{tmp_path.name}-outside.txt"
    outside.write_text("outside\n", encoding="utf-8")
    try:
        (tmp_path / "linked.txt").symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")
    agent = build_agent(tmp_path, [])

    result = agent.run_tool("read_file", {"path": "linked.txt"})

    assert "path escapes workspace" in result


def test_risky_tool_deny_behavior(tmp_path):
    agent = build_agent(tmp_path, [], approval_policy="never")

    result = agent.run_tool("run_shell", {"command": "echo hi", "timeout": 20})

    assert result == "error: approval denied for run_shell"


def test_cli_build_agent_wires_secret_env_names_from_parser(tmp_path):
    class DummyModelClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def complete(self, prompt, max_new_tokens):
            raise AssertionError("model should not be invoked")

    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    with patch.dict(os.environ, {"GITHUB_PAT": "ghp-1", "GH_PAT": "ghp-2"}, clear=True), patch(
        "niko_agent.cli.OpenAICompatibleModelClient",
        DummyModelClient,
    ):
        args = niko_agent_cli.build_arg_parser().parse_args(
            [
                "--cwd",
                str(tmp_path),
                "--approval",
                "auto",
                "--secret-env-name",
                "GITHUB_PAT",
                "--secret-env-name",
                "GH_PAT",
            ]
        )
        agent = niko_agent_cli.build_agent(args)
        assert set(agent.secret_env_summary()["secret_env_names"]) == {"GITHUB_PAT", "GH_PAT"}


def test_cli_build_agent_uses_default_configured_secret_names(tmp_path):
    class DummyModelClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def complete(self, prompt, max_new_tokens):
            raise AssertionError("model should not be invoked")

    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    with patch.dict(os.environ, {"GH_PAT": "ghp-default-1"}, clear=True), patch(
        "niko_agent.cli.OpenAICompatibleModelClient",
        DummyModelClient,
    ):
        args = niko_agent_cli.build_arg_parser().parse_args(["--cwd", str(tmp_path), "--approval", "auto"])
        agent = niko_agent_cli.build_agent(args)
        assert agent.secret_env_summary()["secret_env_names"] == ["GH_PAT"]


def test_cli_build_agent_loads_project_env_secrets_before_redaction_setup(tmp_path):
    class DummyModelClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def complete(self, prompt, max_new_tokens):
            raise AssertionError("model should not be invoked")

    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text("NIKO_DEEPSEEK_API_KEY=sk-project-secret\n", encoding="utf-8")
    with patch.dict(os.environ, {}, clear=True), patch("niko_agent.cli.AnthropicCompatibleModelClient", DummyModelClient):
        args = niko_agent_cli.build_arg_parser().parse_args(["--cwd", str(tmp_path), "--provider", "deepseek"])
        agent = niko_agent_cli.build_agent(args)
        assert agent.secret_env_summary()["secret_env_names"] == ["NIKO_DEEPSEEK_API_KEY"]


def test_cli_does_not_inherit_parent_workspace_config_or_env(tmp_path):
    class DummyModelClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def complete(self, prompt, max_new_tokens):
            raise AssertionError("model should not be invoked")

    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "README.md").write_text("demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text(
        "NIKO_API_KEY=parent-env-secret\n", encoding="utf-8"
    )
    (tmp_path / ".niko.toml").write_text(
        'provider = "anthropic"\n', encoding="utf-8"
    )
    workspace = WorkspaceContext.build(
        workspace_root, repo_root_override=workspace_root
    )
    args = niko_agent_cli.build_arg_parser().parse_args(
        ["--cwd", str(workspace_root), "--approval", "auto"]
    )

    with (
        patch.dict(os.environ, {}, clear=True),
        patch("niko_agent.config.DEFAULT_CONFIG_PATH", tmp_path / "missing.toml"),
        patch.object(niko_agent_cli.WorkspaceContext, "build", return_value=workspace),
        patch(
            "niko_agent.cli.AnthropicCompatibleModelClient",
            side_effect=AssertionError("parent config must not select anthropic"),
        ),
        patch(
            "niko_agent.cli.OpenAICompatibleModelClient",
            side_effect=DummyModelClient,
        ) as openai_client,
    ):
        agent = niko_agent_cli.build_agent(args)

        assert "NIKO_API_KEY" not in os.environ
        assert agent.model_client.kwargs["api_key"] == ""
        openai_client.assert_called_once()


def test_cli_provider_key_is_redacted_even_when_not_from_environment(tmp_path):
    class DummyModelClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def complete(self, prompt, max_new_tokens):
            raise AssertionError("model should not be invoked")

    secret = "config-only-secret-123"
    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    args = niko_agent_cli.build_arg_parser().parse_args(
        ["--cwd", str(tmp_path), "--provider", "openai", "--api-key", secret]
    )

    with (
        patch.dict(os.environ, {}, clear=True),
        patch("niko_agent.config.DEFAULT_CONFIG_PATH", tmp_path / "missing.toml"),
        patch(
            "niko_agent.cli.OpenAICompatibleModelClient",
            side_effect=DummyModelClient,
        ),
    ):
        agent = niko_agent_cli.build_agent(args)

    assert secret not in agent.prompt(f"diagnostic text {secret}")
    assert agent.redact_artifact({"error": f"provider failed with {secret}"}) == {
        "error": "provider failed with <redacted>"
    }
    assert secret not in json.dumps(agent.session)
    agent.remember_durable_note(f"remember {secret}")
    memory_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (tmp_path / ".niko" / "memory" / "logs").rglob("*.md")
    )
    assert secret not in memory_text
    assert "<redacted>" in memory_text


def test_cli_build_agent_reads_secret_names_from_environment_config(tmp_path):
    class DummyModelClient:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def complete(self, prompt, max_new_tokens):
            raise AssertionError("model should not be invoked")

    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    with patch.dict(
        os.environ,
        {
            "NIKO_CUSTOM_SECRET": "custom-secret-value",
            "NIKO_SECRET_ENV_NAMES": "NIKO_CUSTOM_SECRET",
        },
        clear=True,
    ), patch("niko_agent.cli.OpenAICompatibleModelClient", DummyModelClient):
        args = niko_agent_cli.build_arg_parser().parse_args(["--cwd", str(tmp_path), "--approval", "auto"])
        agent = niko_agent_cli.build_agent(args)
        assert agent.secret_env_summary()["secret_env_names"] == ["NIKO_CUSTOM_SECRET"]


def test_run_shell_uses_allowlisted_environment_only(tmp_path):
    secret = "shh-allowlist-secret"
    agent = build_agent(tmp_path, [], approval_policy="auto")
    script = 'import os; print(os.getenv("MCA_ALLOWLIST_SECRET", "missing"))'
    command = python_command(script)

    with patch.dict(os.environ, {"MCA_ALLOWLIST_SECRET": secret}, clear=False):
        result = agent.run_tool("run_shell", {"command": command, "timeout": 20})

    assert secret not in result
    assert "missing" in result


def test_bound_tool_methods_call_tools_module(tmp_path):
    agent = build_agent(tmp_path, [], approval_policy="auto")

    with patch("niko_agent.tools.registry.subprocess.run") as fake_run:
        fake_run.return_value = type(
            "Result",
            (),
            {"returncode": 0, "stdout": "toolkit-shell\n", "stderr": ""},
        )()
        shell_result = agent.tool_run_shell({"command": "echo bypass", "timeout": 20})

    assert "toolkit-shell" in shell_result
    fake_run.assert_called_once()
    assert agent.tool_run_shell.__func__.__module__ == "niko_agent.core.runtime"


def test_configured_secret_env_names_are_redacted_in_trace_and_report(tmp_path):
    github_pat = "ghp_configured_secret_123"
    gh_pat = "ghp_configured_secret_456"
    with patch.dict(os.environ, {"GITHUB_PAT": github_pat, "GH_PAT": gh_pat}, clear=True):
        agent = build_agent(
            tmp_path,
            [],
            secret_env_names=("GITHUB_PAT", "GH_PAT"),
        )
        state = TaskState.create(run_id="run_001", task_id="task_001", user_request="Mask configured secrets")
        agent.run_store.start_run(state)

        assert set(agent.secret_env_summary()["secret_env_names"]) == {"GITHUB_PAT", "GH_PAT"}

        payload = {
            "GITHUB_PAT": github_pat,
            "GH_PAT": gh_pat,
            "nested": {"GITHUB_PAT": github_pat, "GH_PAT": gh_pat},
            "list": [github_pat, gh_pat],
        }
        agent.emit_trace(state, "tool_executed", payload)
        agent.run_store.write_report(
            state,
            agent.redact_artifact({"task_state": state.to_dict(), "payload": payload}),
        )

    run_dir = agent.run_store.run_dir(state.run_id)
    trace_text = (run_dir / "trace.jsonl").read_text(encoding="utf-8")
    report_text = (run_dir / "report.json").read_text(encoding="utf-8")

    assert github_pat not in trace_text
    assert gh_pat not in trace_text
    assert github_pat not in report_text
    assert gh_pat not in report_text
    assert trace_text.count("<redacted>") >= 4
    assert report_text.count("<redacted>") >= 4
