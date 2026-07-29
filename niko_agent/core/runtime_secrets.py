"""Runtime secret redaction and shell environment helpers."""

import os
from pathlib import Path

SENSITIVE_ENV_NAME_MARKERS = ("API_KEY", "TOKEN", "SECRET", "PASSWORD")
REDACTED_VALUE = "<redacted>"

if os.name == "nt":
    _SYSTEM_ROOT = os.environ.get("SystemRoot") or os.environ.get("WINDIR") or r"C:\Windows"
    _WINDOWS_SHELL_ENV = {
        "SystemRoot": _SYSTEM_ROOT,
        "ComSpec": os.environ.get("ComSpec")
        or str(Path(_SYSTEM_ROOT) / "System32" / "cmd.exe"),
    }
else:
    _WINDOWS_SHELL_ENV = {}


class RuntimeSecretsMixin:
    @staticmethod
    def looks_sensitive_env_name(name):
        upper = str(name).upper()
        return any(upper == marker or upper.endswith(marker) or upper.endswith(f"_{marker}") for marker in SENSITIVE_ENV_NAME_MARKERS)

    def is_secret_env_name(self, name):
        upper = str(name).upper()
        return upper in self.secret_env_names or self.looks_sensitive_env_name(upper)

    def configured_secret_env_items(self):
        items = [(name, value) for name, value in os.environ.items() if str(name).upper() in self.secret_env_names and value]
        items.sort(key=lambda item: item[0])
        return items

    def detected_secret_env_items(self):
        items = [(name, value) for name, value in os.environ.items() if self.is_secret_env_name(name) and value]
        items.sort(key=lambda item: item[0])
        return items

    def secret_env_summary(self):
        names = [name for name, _ in self.configured_secret_env_items()]
        return {"secret_env_count": len(names), "secret_env_names": names}

    def detected_secret_env_summary(self):
        names = [name for name, _ in self.detected_secret_env_items()]
        return {"secret_env_count": len(names), "secret_env_names": names}

    def redact_text(self, text):
        text = str(text)
        values = {
            value for _, value in self.detected_secret_env_items() if len(value) >= 4
        }
        values.update(getattr(self, "secret_values", ()))
        for value in sorted(values, key=len, reverse=True):
            text = text.replace(value, REDACTED_VALUE)
        return text

    def redact_artifact(self, value, key=None):
        if key and self.is_secret_env_name(key):
            return REDACTED_VALUE
        if isinstance(value, dict):
            return {str(item_key): self.redact_artifact(item_value, key=item_key) for item_key, item_value in value.items()}
        if isinstance(value, list):
            return [self.redact_artifact(item, key=key) for item in value]
        if isinstance(value, tuple):
            return [self.redact_artifact(item, key=key) for item in value]
        if isinstance(value, str):
            return self.redact_text(value)
        return value

    def shell_env(self):
        env = {name: os.environ[name] for name in self.shell_env_allowlist if name in os.environ}
        # Windows requires these non-secret bootstrap paths even when the caller
        # deliberately supplies a minimal/cleared environment.
        env.update({name: value for name, value in _WINDOWS_SHELL_ENV.items() if value})
        env["PWD"] = str(self.root)
        if "PATH" not in env and os.environ.get("PATH"):
            env["PATH"] = os.environ["PATH"]
        return env
