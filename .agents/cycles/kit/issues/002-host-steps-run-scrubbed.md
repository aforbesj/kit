---
status: done
mode: hands-off
priority: tracer
blocked_by: [1]
---
Steps listed under the PRD's `### Host steps` run on the host, not in the sandbox, after the sandbox steps and in PRD order. Each runs with a scrubbed environment: no variable whose name contains `TOKEN`, `SECRET`, `KEY` or `PASSWORD`, or starts with `AWS_`, `GH_`, `GITHUB_` or `ANTHROPIC_`. `HOME` is a fresh empty temporary directory, removed afterwards, and the working directory is the worktree. Results are recorded in `qa.md` like any other step (ADR 0011).

## Acceptance
- [x] `### Host steps` commands run on the host, never inside `docker run`, in PRD order.
- [x] A host step's environment has none of the variables above, with the rest of the environment (for example `PATH`) kept.
- [x] A host step's `HOME` is a fresh empty directory, and its working directory is the worktree.
- [x] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k host
