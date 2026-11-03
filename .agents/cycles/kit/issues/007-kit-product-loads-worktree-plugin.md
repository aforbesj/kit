---
status: todo
mode: hands-off
priority: infra
blocked_by: []
---
When the Product is the Kit (the repo's `pyproject.toml` has `name = "kit-cycle"`), every `claude` launch from `kit once` and `kit run` gets `--plugin-dir <worktree>/src/kit/plugin`. That covers the host, `--local` and the sandbox. Then `/kit:*` skills come from the Cycle's own working copy. Research confirmed that `--plugin-dir` takes priority over the installed `kit@kit`. In every other Product, the command doesn't change (ADR 0010).

## Acceptance
- [ ] In a repo named `kit-cycle`, the commands from `once` (with and without an Issue) and `run` (sandbox and `--local`) include `--plugin-dir <worktree>/src/kit/plugin`.
- [ ] In a repo with any other name, or with no `pyproject.toml`, the commands have no `--plugin-dir`.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k plugin_dir && uv run pyright && uv run ruff check
