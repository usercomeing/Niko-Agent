from pathlib import Path


def test_core_modules_stay_below_entropy_budget():
    root = Path(__file__).resolve().parents[1]
    budgets = {
        "niko_agent/core/runtime.py": 950,
        "niko_agent/core/runtime_events.py": 90,
        "niko_agent/core/runtime_consumers.py": 90,
        "niko_agent/core/artifacts.py": 130,
        "niko_agent/core/task_state.py": 140,
        "niko_agent/core/todo_ledger.py": 120,
        "niko_agent/core/worker_manager.py": 220,
        "niko_agent/core/context_manager.py": 420,
        "niko_agent/core/context_usage.py": 120,
        "niko_agent/core/compact.py": 180,
        "niko_agent/core/engine.py": 470,
        "niko_agent/core/model_errors.py": 100,
        "niko_agent/core/permissions.py": 140,
        "niko_agent/core/tool_policy.py": 90,
        "niko_agent/core/plan_mode.py": 140,
        "niko_agent/core/tool_executor.py": 181,
        "niko_agent/core/tool_profiles.py": 80,
        "niko_agent/core/turn_history.py": 250,
        "niko_agent/features/skills.py": 220,
        "niko_agent/features/skills_bundled.py": 120,
        "niko_agent/features/skills_runtime.py": 140,
        "niko_agent/tools/registry.py": 360,
        "niko_agent/tools/todos.py": 80,
        "niko_agent/tools/agents.py": 90,
    }

    for relative_path, max_lines in budgets.items():
        line_count = len((root / relative_path).read_text(encoding="utf-8").splitlines())
        assert line_count <= max_lines, f"{relative_path} has {line_count} lines, budget is {max_lines}"
