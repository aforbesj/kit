---
status: todo
mode: hands-off
priority: infra
blocked_by: []
---
Stop the sandbox and the host rebuilding each other's `.venv`. In `agent()`, the sandbox command mounts a named Docker volume, `kit-venv-<product>-<area>`, at a fixed path outside the repo, for example `/home/kit/venv`. It also sets `-e UV_PROJECT_ENVIRONMENT=<that path>`. `<product>` is the repo root folder's name and `<area>` is the worktree folder's name, both cut down to characters Docker allows. Docker creates the volume on first use. The repo's `.venv` stays the host's alone.

## Acceptance
- [ ] The sandbox command has `-v kit-venv-<product>-<area>:<path>` and `-e UV_PROJECT_ENVIRONMENT=<path>`.
- [ ] Two Areas of the same Product get two different volume names, and the names are valid Docker volume names.
- [ ] With Docker available: after a sandboxed `uv sync`, the host's `.venv/bin/python` resolves to the same target as before (the test is skipped without Docker).
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k volume && uv run pyright && uv run ruff check
