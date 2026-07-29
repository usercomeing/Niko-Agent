# Niko-Agent

English | [简体中文](README.md)

A lightweight, local, and white-box auditable terminal coding agent.

Niko runs inside the current Git repository and provides a TUI, REPL, and
one-shot CLI. The model proposes actions while the local runtime validates
arguments, applies permissions and sensitive-path policy, executes tools, and
records evidence. Sessions, runs, checkpoints, memory, and rollback recovery
are stored in the repository-private `.niko/` directory.

## Core capabilities

- OpenAI-compatible and Anthropic-compatible provider profiles.
- Controlled file, search, shell, todo, plan, and sub-agent tools.
- Session resume, checkpoints, `/fork`, and token-confirmed workspace rollback.
- Model tools cannot access `.env` files, private keys, cloud credentials, or
  `.niko/` runtime evidence.
- Trace, task state, reports, session events, and deterministic evaluation.
- `off`, `best_effort`, and `required` sandbox policies.

## Install and run

Python 3.10+, Git, and [uv](https://docs.astral.sh/uv/) are required.

```bash
git clone https://github.com/usercomeing/Niko-Agent.git
cd Niko-Agent
uv sync --dev
uv run niko --help
uv run niko
```

Common entry points:

```bash
uv run niko --repl
uv run niko "inspect the first failing test in this repository"
uv run niko --resume latest
uv run niko --sandbox best_effort --approval ask
```

## Provider configuration

Copy the project template. The real configuration is ignored by Git and is
not readable through model file tools.

```bash
cp .niko.toml.example .niko.toml
```

Configuration precedence is CLI arguments, `NIKO_*` environment variables,
`.niko.toml`, then defaults.

```toml
provider = "openai"

[providers.openai]
protocol = "openai"
api_key = ""
base_url = "https://api.openai.com/v1"
model = "gpt-5.4"
```

`NIKO_API_KEY`, `NIKO_BASE_URL`, `NIKO_MODEL`, and `NIKO_PROVIDER` are also
supported.

## Session recovery

```text
/history
/resume latest
/fork latest
/rollback latest
/rollback --confirm <preview-token>
```

`/fork` truncates session history without changing files. The first
`/rollback` call returns only a create/modify/delete preview and a single-use
token that expires in ten minutes. Confirmation revalidates the workspace
fingerprint, writes a recovery backup, and then restores the checkpoint.

Snapshots include Git-tracked and non-ignored files. They always exclude
`.git/`, `.niko/`, ignored files, sensitive paths, and symbolic links. The
limits are 16 MiB per file and 128 MiB per snapshot; an oversized checkpoint
is marked non-restorable and no partial snapshot is retained.

## Security boundaries

- Model tools cannot list, search, read, or modify `.env*`, `.niko.toml`,
  SSH/GPG/cloud credentials, private keys, or `.niko/` runtime state.
- Empty templates named `.env.example`, `.env.sample`, and `.env.template`
  remain accessible.
- Shell commands inherit only allowlisted environment variables. Configured
  secrets are redacted from traces and reports.
- Bubblewrap is unavailable on Windows. `sandbox=required` fails closed;
  `best_effort` records the degradation and continues. Windows best-effort is
  not OS-level isolation.
- Rollback never restores or deletes ignored or sensitive files.

## Verification and evaluation

The default gates are fully offline:

```bash
uv run python scripts/verify.py --profile quick
uv run python scripts/verify.py --profile full
uv run python scripts/evaluate.py --deterministic
```

The real-provider smoke test is separate from the offline gates and requires
an explicit live flag before it can call an external API.

## Project layout

```text
niko_agent/
├── core/          runtime, engine, sessions, checkpoints, rollback
├── tools/         tool registration, arguments, and policy
├── providers/     model protocol adapters
├── features/      memory, skills, and sandbox
├── evaluation/    metrics, benchmarks, and run evidence
└── tui/           Textual interface
```

See `docs/` for more details and
[docs/runtime-artifacts.md](docs/runtime-artifacts.md) for the runtime evidence
layout. Licensing and attribution are in [LICENSE](LICENSE) and
[NOTICE](NOTICE).
