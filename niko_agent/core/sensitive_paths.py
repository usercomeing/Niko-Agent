"""Sensitive workspace path classification shared by tools and recovery."""

from __future__ import annotations

import os
import posixpath


SENSITIVE_BASENAMES = {
    ".env",
    ".envrc",
    ".netrc",
    ".npmrc",
    ".pypirc",
    ".git-credentials",
    ".niko.toml",
    "credentials.json",
    "auth.json",
    "secrets.json",
    "secrets.yaml",
    "secrets.yml",
    "secrets.toml",
}
ALLOWED_ENV_TEMPLATES = {".env.example", ".env.sample", ".env.template"}
SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".jks", ".keystore")


def normalized_parts(raw_path) -> tuple[str, ...]:
    raw = os.fsdecode(os.fspath(raw_path)).replace("\\", "/")
    return tuple(
        part.casefold()
        for part in posixpath.normpath(raw).split("/")
        if part not in {"", "."}
    )


def sensitive_path_reason(raw_path) -> str:
    parts = normalized_parts(raw_path)
    if not parts:
        return ""
    if any(part in {".niko", ".ssh", ".gnupg"} for part in parts):
        return "sensitive_path"
    for parent, child in zip(parts, parts[1:]):
        if (parent, child) in {
            (".aws", "credentials"),
            (".docker", "config.json"),
            (".kube", "config"),
        }:
            return "sensitive_path"
    leaf = parts[-1]
    if leaf in ALLOWED_ENV_TEMPLATES:
        return ""
    if (
        leaf in SENSITIVE_BASENAMES
        or leaf.startswith(".env.")
        or leaf.endswith(SENSITIVE_SUFFIXES)
        or (leaf.startswith("service-account") and leaf.endswith(".json"))
    ):
        return "sensitive_path"
    return ""


def is_sensitive_path(raw_path) -> bool:
    return bool(sensitive_path_reason(raw_path))


def require_non_sensitive_path(raw_path):
    if is_sensitive_path(raw_path):
        raise ValueError("sensitive path is not available to model tools")

