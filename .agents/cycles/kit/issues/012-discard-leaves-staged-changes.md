---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
`stop_dirty` prints `discard: git -C .worktrees/<area> restore . && git -C .worktrees/<area> clean -fd`. `git restore .` resets the working tree from the index, not from `HEAD`. `git clean` skips files that are in the index. So when the agent staged its work and the commit failed, which is the case this Cycle is about (PRD Problem: "work staged but not committed"), the printed discard line changes nothing. The next `kit run` stops on the same dirty tree. Reproduced: with a staged new file and a staged modification, `git restore . && git clean -fd` leaves `git status --porcelain` showing `A  a.txt`, `A  staged_new.txt`, `M  tracked.txt`. The PRD asks for "the exact commands to keep or discard them".

Fix: make discard reset the index too, for example `git -C <tree> reset -q --hard && git -C <tree> clean -fd`, or `git -C <tree> restore --staged --worktree . && git -C <tree> clean -fd`.

## Acceptance
- [ ] Failing test first: in an Area worktree, stage a new file and a change to a tracked file (`git add -A`), call `stop_dirty`, and run the printed `discard:` line from the root with `shell=True`. Afterwards `dirty_files(worktree)` is empty, and an untracked file in the root is untouched.
- [ ] The existing untracked-only discard test (Issue 010) still passes.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k "dirty or discard" && uv run pyright && uv run ruff check
