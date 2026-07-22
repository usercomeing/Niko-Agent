# Repository Guidelines

## Project Structure & Module Organization

The Python package lives in `niko_agent/`. Keep CLI entry points in `niko_agent/cli.py`, UI code in `niko_agent/tui/`, providers in `niko_agent/providers/`, tools in `niko_agent/tools/`, and runtime coordination in `niko_agent/core/`. Tests live in `tests/`; deterministic fixtures and task definitions belong in `benchmarks/`; verification and acceptance runners belong in `scripts/`. Store maintained documentation in `docs/` and dated development reports in `report/`. Do not commit runtime state from `.niko/`, virtual environments, caches, credentials, or generated evaluation artifacts.

## Branch and Delivery Workflow

Develop on a child branch created from `feature/niko-v1`; do not work directly on `main` or the integration branch. Use small, reviewable commits at coherent milestones. Update a dated file under `report/` with completed work, verification evidence, known limitations, and the next action. Push each completed milestone to the matching GitHub branch only after local checks pass.

## Build, Test, and Development Commands

- `uv sync --dev` installs locked runtime and development dependencies.
- `uv run niko --help` verifies the CLI entry point.
- `uv run python scripts/verify.py --profile quick` runs lint and core offline tests.
- `uv run python scripts/verify.py --profile full` runs the complete offline gate.
- `uv run python scripts/evaluate.py --deterministic` runs scripted evaluation without a live provider.
- `uv run ruff check niko_agent tests scripts` runs static checks directly.

## Coding Style & Testing

Use four-space indentation, UTF-8, type hints where they clarify boundaries, `snake_case` for functions and modules, and `PascalCase` for classes. Keep security decisions explicit and fail closed when checkpoint, permission, or sandbox state is unavailable. Tests use pytest and `pytest-asyncio`; name files `test_<feature>.py` and tests `test_<expected_behavior>`. Add regression coverage for every bug fix. Normal gates must not call live providers.

## Commits, Pull Requests, and Security

Follow Conventional Commits, such as `feat(recovery): add rollback preview`, `fix(eval): handle Windows verifier`, or `docs: record gate status`. Pull requests must explain intent, security implications, commands run, remaining failures, and visible UI changes. Never commit `.env`, API keys, `.niko.toml`, `.niko/`, private keys, or provider responses containing secrets.
