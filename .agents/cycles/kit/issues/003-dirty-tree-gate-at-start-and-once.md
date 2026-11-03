---
status: done
mode: hands-off
priority: polish
blocked_by: [2]
---
`kit run` refuses to start on a dirty worktree. It exits non-zero before any agent or sandbox starts, printing the same `dirty tree` message (files, `keep:`, `discard:`, `then: kit run <area>`). When `kit once` ends on a dirty tree, it prints the same Stop reason as a warning and returns `claude`'s exit code unchanged. Add a test that `run` and `once` never call `git add` or `git commit`.

## Acceptance
- [ ] `kit run` on a dirty tree exits non-zero, and no agent command runs.
- [ ] `kit once` on a dirty tree prints the `dirty tree` lines and returns the fake agent's exit code.
- [ ] A test records every subprocess call from `run` and `once` and finds no `git add` and no `git commit`.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k "dirty or no_commit" && uv run pyright && uv run ruff check
