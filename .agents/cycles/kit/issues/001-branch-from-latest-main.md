---
status: todo
mode: hands-off
priority: tracer
blocked_by: []
---
When `workspace` in `src/kit/cli.py` creates a new `cycle/<area>`, it first runs `git fetch origin` in the root and starts the branch from `origin/main` (the `main` key in kit.json, default `main`). If there is no remote, or the fetch fails, it prints a warning, starts from local `main`, and carries on without an error. Tests in `tests/test_cli.py` use a local bare repo as `origin`.

## Acceptance
- [ ] With a remote whose `main` is ahead of the root's local `main`, the new `cycle/<area>` HEAD equals `origin/main`. (test)
- [ ] With no remote, it prints a warning, the branch starts from local `main`, and nothing raises. (test)
- [ ] When the fetch fails (for example, the remote URL points to a missing path), it prints a warning, starts from local `main`, and nothing raises. (test)
- [ ] Existing tests still pass, and typecheck and lint are clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
