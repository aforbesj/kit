---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
`dirty_files(cwd)` reads `git status --porcelain` through `git()`, which returns `stdout.strip()`. Porcelain lines are `XY path`, and for a tracked file with unstaged edits `X` is a space (` M tracked.txt`). The strip removes that leading space from the first line only, so `line[3:]` cuts one character off the path. Reproduced: in a repo where only the committed `tracked.txt` is modified, `cli.dirty_files(repo)` returns `['racked.txt']`. This is the most common dirty tree: the agent edited code and didn't commit. In that case the `dirty tree:` list and the Stop reason detail show a wrong file name (PRD Done when: "prints the `dirty tree` Stop reason with the pass number and the files"). The existing tests only use untracked or staged files, where `X` is not a space, so they pass.

Fix: don't strip porcelain output before slicing. For example, call `subprocess.run` directly in `dirty_files`, or use `git status --porcelain -z` and split on NUL, which also gives the plain path for renames and quoted names.

## Acceptance
- [ ] Failing test first: in an Area worktree, commit `tracked.txt`, change it without staging, and check `cli.dirty_files(tree) == ["tracked.txt"]`. Also check that `kit run`'s dirty-tree Stop reason after a pass that only modifies a tracked file names `tracked.txt` in full.
- [ ] Existing dirty/discard tests still pass.
- [ ] pyright, ruff and pytest pass.

## Verify
uv run pytest -q tests/test_cli.py -k "dirty or discard" && uv run pyright && uv run ruff check
