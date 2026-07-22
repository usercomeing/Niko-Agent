#!/usr/bin/env python3
"""Cross-platform offline verification entrypoint for Niko-Agent."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUICK_TESTS = (
    "tests/test_workspace.py",
    "tests/test_verify.py",
    "tests/test_niko_security_recovery.py",
    "tests/test_run_evidence.py",
    "tests/test_sandbox_config.py",
    "tests/test_sandbox_runner.py",
    "tests/test_run_store.py",
)
RUFF_TIMEOUT_SECONDS = 120
QUICK_TEST_TIMEOUT_SECONDS = 300
FULL_TEST_TIMEOUT_SECONDS = 900
ACCEPTANCE_TIMEOUT_SECONDS = 300
EVALUATION_TIMEOUT_SECONDS = 300


def _terminate_process_tree(process, *, platform_name=None, grace_seconds=5):
    """Stop only the process tree launched by this verifier command."""
    if process.poll() is not None:
        return
    platform_name = platform_name or os.name
    if platform_name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=grace_seconds,
            )
        except (OSError, subprocess.SubprocessError):
            pass
    else:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except (OSError, ProcessLookupError):
            pass
    try:
        process.wait(timeout=grace_seconds)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        if platform_name == "nt":
            process.kill()
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except (OSError, ProcessLookupError):
        pass
    try:
        process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        pass


def run(command, env, timeout):
    print(
        "+",
        subprocess.list2cmdline(command),
        f"[timeout={timeout}s]",
        flush=True,
    )
    popen_kwargs = {"cwd": ROOT, "env": env}
    if os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True
    process = subprocess.Popen(command, **popen_kwargs)
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        print(
            f"Verification command timed out after {timeout}s; stopping PID {process.pid} tree.",
            file=sys.stderr,
            flush=True,
        )
        _terminate_process_tree(process)
        return 124


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run deterministic Niko-Agent verification.")
    parser.add_argument("--profile", choices=("quick", "full"), default="quick")
    args = parser.parse_args(argv)
    env = dict(os.environ)
    temp_root = Path(tempfile.gettempdir()) / "niko-agent-verify"
    temp_root.mkdir(parents=True, exist_ok=True)
    env.update(
        {
            "TMP": str(temp_root),
            "TEMP": str(temp_root),
            "NIKO_ACCEPTANCE_LIVE": "0",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
        }
    )
    commands = [
        (
            [sys.executable, "-m", "ruff", "check", "niko_agent", "tests", "scripts"],
            RUFF_TIMEOUT_SECONDS,
        ),
    ]
    if args.profile == "quick":
        commands.append(
            (
                [sys.executable, "-m", "pytest", "-q", *QUICK_TESTS],
                QUICK_TEST_TIMEOUT_SECONDS,
            )
        )
    else:
        commands.extend(
            [
                (
                    [sys.executable, "-m", "pytest", "-q", "tests"],
                    FULL_TEST_TIMEOUT_SECONDS,
                ),
                (
                    [
                        sys.executable,
                        "scripts/run_real_session_acceptance.py",
                        "--output-dir",
                        str(
                            Path(tempfile.gettempdir())
                            / "niko-real-session-acceptance"
                        ),
                    ],
                    ACCEPTANCE_TIMEOUT_SECONDS,
                ),
                (
                    [sys.executable, "scripts/evaluate.py", "--deterministic"],
                    EVALUATION_TIMEOUT_SECONDS,
                ),
            ]
        )
    for command, timeout in commands:
        code = run(command, env, timeout)
        if code:
            return code
    print(f"Niko-Agent {args.profile} verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
