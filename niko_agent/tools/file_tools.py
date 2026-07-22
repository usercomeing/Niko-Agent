"""Workspace file tools and their model-visible path filtering."""

from __future__ import annotations

import os
import shutil
import subprocess

from ..core.sensitive_paths import is_sensitive_path
from ..core.workspace import IGNORED_PATH_NAMES


def is_active_dream_memory_access(agent, name, raw_path):
    """Allow the internal dream profile to access only curated memory files."""
    if name not in {"list_files", "read_file", "search", "write_file", "patch_file"}:
        return False
    profile = getattr(agent, "active_tool_profile", None)
    if getattr(profile, "name", "") != "dream":
        return False
    try:
        requested = agent.path(raw_path)
        memory_root = agent.path(agent.memory_dir)
        memory_relative = requested.relative_to(memory_root)
    except (OSError, ValueError):
        return False
    return not is_sensitive_path(memory_relative)


def _is_model_visible_path(agent, path, tool_name):
    relative = path.relative_to(agent.root)
    return not is_sensitive_path(relative) or is_active_dream_memory_access(
        agent, tool_name, path
    )


def tool_list_files(agent, args):
    path = agent.path(args.get("path", "."))
    if not path.is_dir():
        raise ValueError("path is not a directory")
    entries = [
        item
        for item in sorted(
            path.iterdir(), key=lambda item: (item.is_file(), item.name.lower())
        )
        if item.name not in IGNORED_PATH_NAMES
        and _is_model_visible_path(agent, item, "list_files")
    ]
    lines = []
    for entry in entries[:200]:
        kind = "[D]" if entry.is_dir() else "[F]"
        lines.append(f"{kind} {entry.relative_to(agent.root).as_posix()}")
    return "\n".join(lines) or "(empty)"


def tool_read_file(agent, args):
    path = agent.path(args["path"])
    if not path.is_file():
        raise ValueError("path is not a file")
    start = int(args.get("start", 1))
    end = int(args.get("end", 200))
    if start < 1 or end < start:
        raise ValueError("invalid line range")
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    body = "\n".join(
        f"{number:>4}: {line}"
        for number, line in enumerate(lines[start - 1 : end], start=start)
    )
    return f"# {path.relative_to(agent.root).as_posix()}\n{body}"


def _searchable_files(agent, path):
    """Return only files the model is allowed to search."""
    if path.is_file():
        return [path]

    ignored_names = {name.casefold() for name in IGNORED_PATH_NAMES}
    files = []
    for current_root, dir_names, file_names in os.walk(path, followlinks=False):
        current = type(path)(current_root)
        safe_dirs = []
        for name in dir_names:
            candidate = current / name
            if (
                name.casefold() not in ignored_names
                and not candidate.is_symlink()
                and _is_model_visible_path(agent, candidate, "search")
            ):
                safe_dirs.append(name)
        dir_names[:] = safe_dirs

        for name in file_names:
            candidate = current / name
            if (
                name.casefold() not in ignored_names
                and not candidate.is_symlink()
                and _is_model_visible_path(agent, candidate, "search")
            ):
                files.append(candidate)
    return sorted(files, key=lambda item: str(item.relative_to(agent.root)).casefold())


def _run_rg_batch(agent, pattern, relative_paths):
    result = subprocess.run(
        [
            "rg", "-n", "--with-filename", "--smart-case", "--max-count", "200",
            "--", pattern, *relative_paths,
        ],
        cwd=agent.root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode not in {0, 1}:
        return [result.stderr.strip() or "search failed"]
    return result.stdout.splitlines()


def _rg_search(agent, pattern, files):
    matches = []
    batch = []
    batch_chars = 0
    for file_path in files:
        relative = file_path.relative_to(agent.root).as_posix()
        if batch and (len(batch) >= 100 or batch_chars + len(relative) > 20_000):
            matches.extend(_run_rg_batch(agent, pattern, batch))
            if len(matches) >= 200:
                return "\n".join(matches[:200])
            batch = []
            batch_chars = 0
        batch.append(relative)
        batch_chars += len(relative) + 1
    if batch:
        matches.extend(_run_rg_batch(agent, pattern, batch))
    return "\n".join(matches[:200]) or "(no matches)"


def tool_search(agent, args):
    pattern = str(args.get("pattern", "")).strip()
    if not pattern:
        raise ValueError("pattern must not be empty")
    path = agent.path(args.get("path", "."))
    files = _searchable_files(agent, path)

    if shutil.which("rg"):
        return _rg_search(agent, pattern, files)

    matches = []
    for file_path in files:
        for number, line in enumerate(
            file_path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
        ):
            if pattern.lower() in line.lower():
                relative = file_path.relative_to(agent.root).as_posix()
                matches.append(f"{relative}:{number}:{line}")
                if len(matches) >= 200:
                    return "\n".join(matches)
    return "\n".join(matches) or "(no matches)"


def tool_write_file(agent, args):
    path = agent.path(args["path"])
    content = str(args["content"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    relative = path.relative_to(agent.root).as_posix()
    return f"wrote {relative} ({len(content)} chars)"


def tool_patch_file(agent, args):
    path = agent.path(args["path"])
    if not path.is_file():
        raise ValueError("path is not a file")
    old_text = str(args.get("old_text", ""))
    if not old_text:
        raise ValueError("old_text must not be empty")
    if "new_text" not in args:
        raise ValueError("missing new_text")
    text = path.read_text(encoding="utf-8")
    count = text.count(old_text)
    if count != 1:
        raise ValueError(f"old_text must occur exactly once, found {count}")
    path.write_text(text.replace(old_text, str(args["new_text"]), 1), encoding="utf-8")
    return f"patched {path.relative_to(agent.root).as_posix()}"
