---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
After every agent pass in `kit run` (implement and review), check `git status --porcelain` in the worktree. If anything is uncommitted, stop before the next pass with the `dirty tree` Stop reason. Its detail gives the pass number and the uncommitted files, followed by these lines:
- `keep:    git add -A && git commit -m "<n>: <title>"`
- `discard: git restore . && git clean -fd`
- `then: kit run <area>`

Exit non-zero. `kit` never stages or commits anything itself (ADR 0009).

## Acceptance
- [ ] A fake agent that leaves an untracked or staged file stops `run` after that pass. No further pass starts.
- [ ] The output has `dirty tree`, the pass number, every file, and the `keep:`, `discard:` and `then:` lines. The exit code is non-zero.
- [ ] A fake agent that commits cleanly carries on as before.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k dirty && uv run pyright && uv run ruff check
