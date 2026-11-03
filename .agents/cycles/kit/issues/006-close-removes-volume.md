---
status: todo
mode: hands-off
priority: polish
blocked_by: [5]
---
`kit close` (both the merge path and `--abandon`) removes the Area's `kit-venv-<product>-<area>` volume when it frees the worktree. It uses the same name function as 005. It succeeds when the volume doesn't exist, Docker isn't installed, or Docker isn't running, so finished Cycles leave no volumes behind.

## Acceptance
- [ ] `close` runs `docker volume rm kit-venv-<product>-<area>` on both paths.
- [ ] A missing volume, a missing `docker` or a stopped Docker doesn't change `close`'s exit code.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k close && uv run pyright && uv run ruff check
