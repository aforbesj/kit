---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
The PRD's Done when includes "After a sandboxed `kit run`, the host's `.venv/bin/python` points where it did before. (test)" Issue 005 had it as an Acceptance box ("skipped without Docker"). That test was never written (progress.txt, 005). Today only the command shape is tested, so nothing checks that `uv` inside the container really leaves the bind-mounted repo `.venv` alone.

## Acceptance
- [ ] Failing test first: a test marked to skip when `docker info` fails. It records `os.path.realpath` of a worktree's `.venv/bin/python`, runs `uv sync` through the exact `cli.agent(..., hands_off=True, local=False)` docker command (with the agent swapped for `uv sync`), then asserts the realpath is unchanged and the `kit-venv-<product>-<area>` volume now exists. It removes the volume afterwards.
- [ ] Without Docker the test is skipped, and `uv run pytest -q` still runs in seconds.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k venv && uv run pyright && uv run ruff check
