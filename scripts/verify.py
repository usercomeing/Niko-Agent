#!/usr/bin/env python3
"""Cross-platform offline verification entrypoint for Niko-Agent."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUICK_TESTS = (
    "tests/test_niko_security_recovery.py",
    "tests/test_run_evidence.py",
    "tests/test_sandbox_config.py",
    "tests/test_sandbox_runner.py",
    "tests/test_run_store.py",
)


def run(command, env):
    print("+", subprocess.list2cmdline(command), flush=True)
    return subprocess.run(command, cwd=ROOT, env=env).returncode


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run deterministic Niko-Agent verification.")
    parser.add_argument("--profile", choices=("quick", "full"), default="quick")
    args = parser.parse_args(argv)
    env = dict(os.environ)
    temp_root = Path(tempfile.gettempdir()) / "niko-agent-verify"
    temp_root.mkdir(parents=True, exist_ok=True)
    env.update({"TMP": str(temp_root), "TEMP": str(temp_root), "NIKO_ACCEPTANCE_LIVE": "0"})
    commands = [
        [sys.executable, "-m", "ruff", "check", "niko_agent", "tests", "scripts"],
        [sys.executable, "-m", "pytest", "-q", *QUICK_TESTS],
    ]
    if args.profile == "full":
        commands.extend(
            [
                [sys.executable, "-m", "pytest", "-q", "tests"],
                [
                    sys.executable,
                    "scripts/run_real_session_acceptance.py",
                    "--output-dir",
                    str(Path(tempfile.gettempdir()) / "niko-real-session-acceptance"),
                ],
                [sys.executable, "scripts/evaluate.py", "--deterministic"],
            ]
        )
    for command in commands:
        code = run(command, env)
        if code:
            return code
    print(f"Niko-Agent {args.profile} verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
