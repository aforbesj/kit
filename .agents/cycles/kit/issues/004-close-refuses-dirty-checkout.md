---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
`close` in `src/kit/cli.py` first checks the Area's checkout with `git status --porcelain`. If there are uncommitted changes, it prints a message telling the human to commit or discard them and returns 1. It does this with or without `--abandon`, and before it tags, rebases, pushes or removes anything.

## Acceptance
- [ ] `kit close <area>` on a checkout with uncommitted changes returns 1, and the checkout, its changes and the remote are unchanged. (test)
- [ ] `kit close <area> --abandon` on a checkout with uncommitted changes returns 1, creates no tag, and leaves the checkout, its changes and the branch unchanged. (test)
- [ ] Typecheck and lint are clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
