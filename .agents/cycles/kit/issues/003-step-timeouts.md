---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
Every QA step, sandbox or host, has a timeout: 300 s by default, or the step's own `timeout:` (case-insensitive, for example `Timeout: 10m` or `timeout: 1s`, in s or m). A step that runs past it is killed with its whole process tree (its own process group, or the container for sandbox steps), counts as failed, and is recorded in `qa.md` as timed out with its duration.

## Acceptance
- [ ] A step with no `timeout:` is killed at 300 s; one with `timeout: 1s` at 1 s; `Timeout: 10m` parses as 600 s.
- [ ] After a timeout, none of the step's child processes are left running.
- [ ] A timed-out step counts as failed and `qa.md` says it timed out.
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass.

## Verify
uv run pytest -q tests/test_cli.py -k timeout
