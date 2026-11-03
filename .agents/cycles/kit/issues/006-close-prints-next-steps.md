---
status: done
mode: hands-off
priority: polish
blocked_by: [4]
---
A successful `kit close <area>` ends by printing the next steps in order: merge the PR (or `git merge --no-ff` with no remote), then `kit once <area>`, then `/kit:grill`. The message replaces the current closing message in both the remote and the no-remote path.

## Acceptance
- [ ] A successful `kit close <area>` prints the merge step, `kit once <area>` and `/kit:grill`, in that order. (test)
- [ ] Typecheck and lint are clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
