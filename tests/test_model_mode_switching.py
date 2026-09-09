"""Regression coverage through the real CLI composition and command boundary."""

import io
import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from niko_agent import config
from niko_agent.cli import build_agent, build_arg_parser, handle_repl_command
from niko_agent.core.worker_runtime import build_child_runtime
from niko_agent.providers import AnthropicCompatibleModelClient


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEFAULT_CONFIG_PATH", tmp_path / "user.toml")
    from niko_agent.core.workspace import WorkspaceContext

    real_build = WorkspaceContext.build
    monkeypatch.setattr(
        WorkspaceContext,
        "build",
        lambda cwd, **kwargs: real_build(cwd, repo_root_override=cwd),
    )
    with patch.dict(os.environ, {}, clear=True):
        (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
        (tmp_path / ".niko.toml").write_text(
            'provider = "openai"\n'
            '[providers.openai]\napi_key = "test-openai-key"\n'
            'base_url = "https://openai.example/v1"\nmodel = "old-model"\n'
            '[providers.deepseek]\napi_key = "test-deepseek-key"\n'
            'base_url = "https://deepseek.example/anthropic"\n'
            'model = "deepseek-v4-pro"\n'
            '[providers.anthropic]\napi_key = "test-anthropic-key"\n'
            '[providers.custom]\nprotocol = "openai"\n'
            'api_key = "test-custom-key"\nbase_url = "https://custom.example/v1"\n'
            'model = "custom-default"\n',
            encoding="utf-8",
        )
        yield tmp_path


def make_agent(workspace, *options):
    args = build_arg_parser().parse_args(
        ["--cwd", str(workspace), "--no-auto-dream", *options]
    )
    return build_agent(args)


@pytest.mark.parametrize("target", ["deepseek", "dpsk"])
def test_provider_switch_routes_real_request_and_new_child(workspace, target):
    agent = make_agent(workspace)
    old_client = agent.model_client
    config_before = (workspace / ".niko.toml").read_bytes()
    agent.last_completion_metadata = {"input_tokens": 123}
    handled, exit_requested, output = handle_repl_command(agent, f"/model {target}")
    assert handled and not exit_requested
    assert "deepseek-v4-pro" in output
    assert agent.model_client is not old_client
    assert isinstance(agent.model_client, AnthropicCompatibleModelClient)
    assert agent.model_client.api_key == "test-deepseek-key"
    response = io.BytesIO(b'{"content":[{"type":"text","text":"<final>ok</final>"}]}')
    with patch("urllib.request.urlopen", return_value=response) as request:
        assert agent.model_client.complete("minimal probe", 32) == "<final>ok</final>"
    outgoing = request.call_args.args[0]
    assert outgoing.full_url == "https://deepseek.example/anthropic/v1/messages"
    assert outgoing.get_header("X-api-key") == "test-deepseek-key"
    assert json.loads(outgoing.data)["model"] == "deepseek-v4-pro"
    child = build_child_runtime(agent, "Explore", ())
    assert child.model_client is not agent.model_client
    assert child.model_client.api_key == "test-deepseek-key"
    assert child.model_client.model == agent.model_client.model
    assert child.model_client.base_url == agent.model_client.base_url
    assert "test-deepseek-key" not in agent.redact_text("test-deepseek-key")
    assert "test-openai-key" not in agent.redact_text("test-openai-key")
    assert agent.last_completion_metadata == {}
    assert (workspace / ".niko.toml").read_bytes() == config_before


def test_model_name_switch_updates_factory_and_explicit_model(workspace):
    agent = make_agent(workspace)
    assert (
        handle_repl_command(agent, "/model another-model")[2] == "model: another-model"
    )
    assert agent.model_client_factory().model == "another-model"
    assert agent.model_client.api_key == "test-openai-key"
    assert "fast-model" in handle_repl_command(agent, "/model custom fast-model")[2]
    assert agent.model_client_factory().model == "fast-model"
    assert agent.model_client.api_key == "test-custom-key"


@pytest.mark.parametrize("source", ["env", "dotenv", "cli"])
def test_switch_does_not_forward_old_generic_credentials(
    workspace, monkeypatch, source
):
    options = []
    values = {
        "NIKO_API_KEY": "old-private-key",
        "NIKO_BASE_URL": "https://old.example/v1",
        "NIKO_MODEL": "old-override",
        "NIKO_PROTOCOL": "openai",
    }
    if source == "env":
        for key, value in values.items():
            monkeypatch.setenv(key, value)
    elif source == "dotenv":
        path = workspace / ".niko.toml"
        path.write_text(
            path.read_text(encoding="utf-8").replace('api_key = "test-openai-key"', ""),
            encoding="utf-8",
        )
        (workspace / ".env").write_text(
            "\n".join(f"{key}={value}" for key, value in values.items()),
            encoding="utf-8",
        )
    else:
        options = [
            "--api-key",
            values["NIKO_API_KEY"],
            "--base-url",
            values["NIKO_BASE_URL"],
            "--model",
            values["NIKO_MODEL"],
        ]
    agent = make_agent(workspace, *options)
    assert agent.model_client.api_key == "old-private-key"
    handle_repl_command(agent, "/model dpsk")
    assert isinstance(agent.model_client, AnthropicCompatibleModelClient)
    assert agent.model_client.api_key == "test-deepseek-key"
    assert agent.model_client.model == "deepseek-v4-pro"
    assert agent.model_client.base_url.startswith("https://deepseek.example/")
    handle_repl_command(agent, "/model openai")
    assert agent.model_client.api_key == "old-private-key"
    assert agent.model_client.model == (
        "old-model" if source == "dotenv" else "old-override"
    )


def test_raw_configuration_error_does_not_echo_credentials(workspace):
    agent = make_agent(workspace)
    before = agent.model_client
    (workspace / ".env").write_text("private-secret-without-equals", encoding="utf-8")
    output = handle_repl_command(agent, "/model deepseek")[2]
    assert output.startswith("error:")
    assert "private-secret-without-equals" not in output
    assert agent.model_client is before


@pytest.mark.parametrize("real_environment", [False, True])
def test_dotenv_profile_values_stay_below_toml_on_switch(
    workspace, monkeypatch, real_environment
):
    (workspace / ".env").write_text(
        "DEEPSEEK_BASE_URL=https://legacy.example/anthropic\n"
        "DEEPSEEK_MODEL=legacy-model\n",
        encoding="utf-8",
    )
    if real_environment:
        monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://process.example/anthropic")
    agent = make_agent(workspace)
    # Exercise the actual startup import that used to promote legacy values.
    assert os.environ["DEEPSEEK_MODEL"] == "legacy-model"
    assert "deepseek-v4-pro" in handle_repl_command(agent, "/model dpsk")[2]
    expected = "process.example" if real_environment else "deepseek.example"
    assert agent.model_client.base_url == f"https://{expected}/anthropic/v1"
    assert agent.model_client.api_key == "test-deepseek-key"
    assert agent.model_client_factory().base_url == agent.model_client.base_url


def test_switch_keeps_dotenv_key_as_fallback(workspace):
    path = workspace / ".niko.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('api_key = "test-deepseek-key"', ""),
        encoding="utf-8",
    )
    (workspace / ".env").write_text(
        "DEEPSEEK_API_KEY=legacy-test-key\n", encoding="utf-8"
    )
    agent = make_agent(workspace)
    assert "deepseek-v4-pro" in handle_repl_command(agent, "/model deepseek")[2]
    assert agent.model_client.api_key == "legacy-test-key"


def test_same_provider_keyless_model_switch_remains_supported(workspace):
    path = workspace / ".niko.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('api_key = "test-openai-key"', ""),
        encoding="utf-8",
    )
    agent = make_agent(workspace)
    assert not agent.model_client.api_key
    assert handle_repl_command(agent, "/model local-model")[2] == "model: local-model"
    assert agent.model_client_factory().model == "local-model"


def test_missing_target_key_and_unknown_provider_preserve_connection(workspace):
    agent = make_agent(workspace)
    old = agent.model_client
    old_factory = agent.model_client_factory
    path = workspace / ".niko.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('api_key = "test-deepseek-key"', ""),
        encoding="utf-8",
    )
    for command in ["/model deepseek", "/model nonexistent some-model"]:
        handled, _, output = handle_repl_command(agent, command)
        assert handled and output.startswith("error:")
        assert agent.model_client is old
        assert agent.model_client_factory is old_factory
    assert "API Key" in handle_repl_command(agent, "/model deepseek")[2]


@pytest.mark.parametrize("failure", ["builder", "event", "prefix"])
def test_switch_failure_keeps_previous_connection(workspace, monkeypatch, failure):
    agent = make_agent(workspace)
    before = (
        agent.model_client,
        agent.model_client_factory,
        agent.max_new_tokens,
        agent.prefix,
    )

    def fail(*args, **kwargs):
        raise ValueError("injected failure")

    if failure == "builder":
        monkeypatch.setattr("niko_agent.cli.AnthropicCompatibleModelClient", fail)
    elif failure == "event":
        monkeypatch.setattr(agent.session_event_bus, "emit", fail)
    else:
        monkeypatch.setattr(agent, "refresh_prefix", fail)
    assert handle_repl_command(agent, "/model deepseek")[2].startswith("error:")
    assert (
        agent.model_client,
        agent.model_client_factory,
        agent.max_new_tokens,
        agent.prefix,
    ) == before


@pytest.mark.parametrize("explicit, expected", [(False, 32000), (True, 777)])
def test_switch_respects_explicit_token_budget(workspace, explicit, expected):
    agent = make_agent(workspace, *(["--max-new-tokens", "777"] if explicit else []))
    handle_repl_command(agent, "/model anthropic")
    assert agent.max_new_tokens == expected
    assert build_child_runtime(agent, "Explore", ()).max_new_tokens == expected


def test_mode_commands_persist_and_enforce_plan_permissions(workspace):
    agent = make_agent(workspace)
    handled, _, output = handle_repl_command(agent, "/mode plan review authentication")
    assert handled and "mode: plan" in output
    assert agent.runtime_mode == "plan"
    assert agent.plan_mode.state["topic"] == "review authentication"
    assert (
        agent.session_store.load(agent.session["id"])["runtime_mode"]["mode"] == "plan"
    )
    with pytest.raises(ValueError, match="plan mode only allows Explore"):
        agent.worker_manager.spawn("worker", "change code", write_scope=["README.md"])
    assert handle_repl_command(agent, "/mode default")[2] == "mode: default"
    assert agent.runtime_mode == "default"
    assert handle_repl_command(agent, "/plan legacy")[0]
    assert agent.runtime_mode == "plan"
    assert handle_repl_command(agent, "/plan-exit")[2] == "mode: default"


@pytest.mark.parametrize(
    "command", ["/mode invalid", "/mode default extra", "/mode plan"]
)
def test_invalid_mode_arguments_are_handled_without_changing_state(workspace, command):
    agent = make_agent(workspace)
    handled, _, output = handle_repl_command(agent, command)
    assert handled and "Usage:" in output
    assert agent.runtime_mode == "default"


def test_user_configuration_and_project_override_stay_workspace_local(
    workspace, monkeypatch
):
    shared = workspace / "shared.toml"
    shared.write_text(
        (workspace / ".niko.toml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    monkeypatch.setattr(config, "DEFAULT_CONFIG_PATH", shared)
    first, second = workspace / "a", workspace / "b"
    first.mkdir()
    second.mkdir()
    (first / ".niko.toml").write_text('provider = "deepseek"\n', encoding="utf-8")
    a, b = make_agent(first), make_agent(second)
    assert a.model_client.api_key == "test-deepseek-key"
    assert b.model_client.api_key == "test-openai-key"
    assert Path(a.session_path).is_relative_to(first)
    assert Path(b.session_path).is_relative_to(second)
