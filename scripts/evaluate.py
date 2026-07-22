#!/usr/bin/env python3
"""Run Niko-Agent's deterministic harness benchmark without a live provider."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from niko_agent.evaluation.evaluator import run_harness_regression_v2  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run deterministic Niko-Agent evaluation.")
    parser.add_argument("--deterministic", action="store_true", help="Required safety flag; no provider calls are made.")
    parser.add_argument("--output", default="artifacts/evaluation/harness-regression-v2.json")
    args = parser.parse_args(argv)
    if not args.deterministic:
        parser.error("pass --deterministic; live evaluation is intentionally separate")
    output = (ROOT / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    artifact = run_harness_regression_v2(
        benchmark_path=ROOT / "benchmarks" / "coding_tasks.json",
        artifact_path=output,
        workspace_root=output.parent / "workspaces",
    )
    summary = artifact.get("summary", {})
    print(json.dumps({"artifact": str(output), "summary": summary}, ensure_ascii=False, sort_keys=True))
    return 0 if summary.get("failed", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

