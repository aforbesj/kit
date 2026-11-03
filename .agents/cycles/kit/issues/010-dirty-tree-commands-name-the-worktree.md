---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
`stop_dirty` prints `keep:    git add -A && git commit ...` and `discard: git restore . && git clean -fd` with no directory. `kit run` is started from the repo root, but the dirty files are in `.worktrees/<area>`. If you paste either line into the same shell, it acts on the root checkout: `keep` commits on the root's branch (usually `main`), and `discard` throws away the root's own uncommitted work. The PRD asks for "the exact commands to keep or discard them". Name the worktree in each command, for example `git -C .worktrees/<area> add -A && git -C .worktrees/<area> commit -m "<n>: <title>"`. Do the same for `discard`. `then: kit run <area>` stays as it is.

## Acceptance
- [ ] Failing test first: after the dirty-tree stop in `test_run_stops_when_a_pass_leaves_files`, the `keep:` and `discard:` lines each target `.worktrees/core` (`-C .worktrees/core` or a leading `cd .worktrees/core &&`). Running the printed `discard:` line from the root with `shell=True` removes `stray.txt` from the worktree and leaves an untracked file in the root alone.
- [ ] The start gate and `kit once` print the same worktree-targeted lines.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k dirty && uv run pyright && uv run ruff check
