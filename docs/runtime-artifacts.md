# Runtime artifacts and execution flow

Niko keeps resumable state and per-request audit evidence separate. All
runtime data is local to the active workspace under `.niko/` and is ignored by
Git.

## Directory layout

```text
.niko/
├── sessions/
│   ├── <session-id>.json          resumable session state
│   └── <session-id>.events.jsonl  append-only session timeline
├── runs/
│   └── <run-id>/
│       ├── task_state.json        terminal status and stop reason
│       ├── trace.jsonl            per-request event stream
│       ├── report.json            final audit summary
│       └── artifacts/             bounded full-output spill files
├── checkpoints/
│   └── <checkpoint-id>/
│       ├── manifest.json          file sizes and SHA-256 hashes
│       └── files/                 complete restorable snapshot
├── recovery/
│   └── <operation-id>/
│       ├── journal.json           rollback phase and compensation status
│       ├── manifest.json          pre-rollback backup manifest
│       ├── report.json            redacted rollback outcome
│       └── files/                 pre-rollback workspace backup
├── memory/                        durable local memory
└── plans/                         active plan-mode artifacts
```

Checkpoint and recovery snapshots contain only Git-visible regular files.
They exclude `.git/`, `.niko/`, Git-ignored files, sensitive paths, and
symbolic links. Model file tools cannot access `.niko/`.

## Execution flow

1. The CLI resolves the Git workspace root, reads only that workspace's local
   `.env` and `.niko.toml` (plus an explicitly selected or user-level Niko
   config), builds the provider client, and creates or resumes a session.
2. Each `ask()` creates a task state and `.niko/runs/<run-id>/` before model
   execution. Prompt metadata records workspace and resume identity without
   configuration values.
3. Tool calls pass schema validation, sensitive-path checks, tool policy,
   permissions, and sandbox policy before execution. Tool results and errors
   are redacted before trace/report persistence.
4. Successful state transitions create a checkpoint. A rollback-capable
   checkpoint is marked available only after its complete snapshot and
   manifest have been written within the 16 MiB per-file and 128 MiB total
   limits.
5. `/fork` creates a history-truncated child session without touching files.
   `/rollback` first emits a tokenless preview event. Confirmation consumes the
   one-use token, revalidates the workspace and snapshot, backs up the current
   workspace, writes a journal, restores the checkpoint, and creates a child
   session. Any interruption triggers best-effort compensation and leaves a
   redacted recovery report.

## Offline verification outputs

- `scripts/verify.py --profile quick` runs Ruff and the focused offline safety
  suite.
- `scripts/verify.py --profile full` runs Ruff, all pytest tests, deterministic
  real-session acceptance, and deterministic evaluation. Every phase has a
  timeout and the verifier only cleans up its own child process tree.
- `scripts/run_real_session_acceptance.py` writes JSON/Markdown summaries plus
  scenario run evidence to its selected output directory.
- `scripts/evaluate.py --deterministic` writes the benchmark result under
  `artifacts/evaluation/` by default. Generated acceptance and evaluation
  artifacts are intentionally not committed.

The real-provider smoke test is not part of these offline gates. It requires a
separate explicit live flag and user authorization.
