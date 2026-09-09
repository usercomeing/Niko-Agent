"""Interactive model selection without persisting credentials or preferences."""

from collections.abc import Callable, Mapping
from dataclasses import replace

from .config import (
    ProviderConfig,
    configured_provider_names,
    default_max_tokens_for_provider,
    normalize_provider_name,
    resolve_provider_config,
)


class ModelSelectionError(ValueError):
    """Safe, user-facing selection validation errors (never raw config errors)."""


class ModelSelection:
    def __init__(
        self,
        config: ProviderConfig,
        build_client: Callable,
        *,
        root: str,
        config_path: str | None,
        automatic_token_budget: bool,
        environment: Mapping[str, str],
    ):
        self.current = config
        self._configs = {config.name: config}
        self._build_client = build_client
        self._root = root
        self._config_path = config_path
        self._automatic_token_budget = automatic_token_budget
        # Preserve provenance: CLI later imports .env into os.environ for tools,
        # but those fallback values must never outrank the selected TOML profile.
        self._environment = dict(environment)

    def switch(self, agent, target: str) -> str:
        parts = target.split()
        if not parts or len(parts) > 2:
            raise ModelSelectionError("Usage: /model [<model> | <provider> [model]]")
        provider = normalize_provider_name(parts[0])
        names = configured_provider_names(self._root, self._config_path) | set(
            self._configs
        )
        if provider in names:
            config = self._configs.get(provider)
            if config is None:
                config = resolve_provider_config(
                    provider,
                    start=self._root,
                    config_path=self._config_path,
                    search_parents=False,
                    include_generic_env=False,
                    environment=self._environment,
                )
            if len(parts) == 2:
                config = replace(config, model=parts[1])
        elif len(parts) == 1:
            config = replace(self.current, model=parts[0])
        else:
            raise ModelSelectionError(
                "Unknown provider. Usage: /model <provider> [model]"
            )
        if config.name != self.current.name and not config.api_key.strip():
            raise ModelSelectionError(
                "目标 provider 缺少 API Key；请配置对应的 provider profile。"
            )

        # Construct everything before touching the active connection. The factory
        # captures this immutable profile so existing child runtimes keep theirs.
        candidate = self._build_client(config)

        def factory():
            return self._build_client(config)

        secrets = set(agent.secret_values)
        if len(config.api_key) >= 4:
            secrets.add(config.api_key)
        # Snapshot the fields touched by refresh_prefix as well as the connection.
        fields = (
            "model_client",
            "model_client_factory",
            "max_new_tokens",
            "secret_values",
            "last_completion_metadata",
            "last_prompt_metadata",
            "workspace",
            "prefix",
            "prefix_state",
            "_last_prefix_refresh",
        )
        previous = {name: getattr(agent, name) for name in fields}
        try:
            agent.model_client = candidate
            agent.model_client_factory = factory
            agent.secret_values = tuple(sorted(secrets, key=len, reverse=True))
            if self._automatic_token_budget:
                agent.max_new_tokens = default_max_tokens_for_provider(config.name)
            agent.last_completion_metadata = {}
            agent.last_prompt_metadata = {}
            agent.refresh_prefix(force=True)
            agent.session_event_bus.emit(
                "model_changed", {"model": config.model, "provider": config.name}
            )
        except Exception:
            for name, value in previous.items():
                setattr(agent, name, value)
            raise
        self.current = config
        self._configs[config.name] = config
        return config.model
