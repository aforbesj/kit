---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
When the Product is the Kit, `kit run` hands off to the worktree's CLI through `subprocess.run` in `hand_off`. Ctrl-C reaches both processes: the child prints `Stop reason: interrupted: Ctrl-C`, then the parent's `subprocess.run` re-raises `KeyboardInterrupt` and prints a traceback. The last line is no longer the Stop reason. The same happens for a Ctrl-C during `sandbox()` (the first image build can take minutes), `workspace()` or the start gate, because the `try` in `run` only covers the pass loop. Every way `kit run` ends must print exactly one Stop reason as its last line (PRD Done when).

## Acceptance
- [ ] Failing test first: with `pyproject` name `kit-cycle`, `KIT_SELF` unset and `subprocess.run` faked to raise `KeyboardInterrupt`, `cli.main(["run", "core", "--local"])` returns 130 and raises nothing. The parent prints no second Stop reason, because the child already printed one.
- [ ] Failing test first: with `sandbox` (or `workspace`) faked to raise `KeyboardInterrupt`, `cli.run(...)` returns 130 and its last line is `Stop reason: interrupted: Ctrl-C`.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k interrupt && uv run pyright && uv run ruff check
