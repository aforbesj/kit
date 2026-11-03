---
status: todo
mode: hands-off
priority: infra
blocked_by: [7]
---
When the Product is the Kit, `kit once` and `kit run` hand off to the worktree's own CLI: `uv run --project <worktree> kit <same args>`, with `KIT_SELF=1` set so the handed-off CLI doesn't hand off again. That way prompts, gates and Stop reasons come from the code this Cycle is changing. `kit` returns the handed-off process's exit code. Every other Product, and `KIT_SELF=1`, runs in-process as today (ADR 0010).

## Acceptance
- [ ] In a repo named `kit-cycle` without `KIT_SELF`, `once` and `run` run `uv run --project <worktree> kit …` with the same arguments and `KIT_SELF=1`, and return its exit code.
- [ ] With `KIT_SELF=1`, or in any other Product, there is no hand-off.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k self_host && uv run pyright && uv run ruff check
