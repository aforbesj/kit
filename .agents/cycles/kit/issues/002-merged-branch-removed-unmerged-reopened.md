---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
When `cycle/<area>` already exists and no checkout is present, `workspace` checks whether the branch is merged into `origin/main` (or local `main` when there is no remote). If it is merged, it deletes the branch locally and on the remote, then creates a new one from the latest `main` as in 001. If it is not merged, it reopens the branch with its commits intact, deletes nothing, and prints "Cycle still open: not merged into `main`". A squash-merged branch counts as unmerged.

## Acceptance
- [ ] With `cycle/<area>` merged into `main` by a merge commit, creating the checkout deletes the old branch locally and on the remote, and the new `cycle/<area>` HEAD equals the latest `origin/main`. (test)
- [ ] With an unmerged `cycle/<area>`, creating the checkout reopens it with its commits intact, deletes nothing locally or remotely, and prints "Cycle still open: not merged into `main`". (test)
- [ ] Typecheck and lint are clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
