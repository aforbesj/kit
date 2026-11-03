---
status: done
mode: hands-off
priority: tracer
blocked_by: [1]
---
After a successful fetch, when `workspace` creates a checkout and the root checkout is clean and on `main`, it fast-forwards the root to `origin/main` (`git merge --ff-only`). If the root is dirty or on another branch, it leaves the root alone. In every case the new Cycle Branch starts from `origin/main`.

## Acceptance
- [ ] With the root clean and on `main`, creating the checkout fast-forwards the root's `main` to `origin/main`. (test)
- [ ] With the root dirty, its HEAD, branch and changes are unchanged, and the new Cycle Branch HEAD equals `origin/main`. (test)
- [ ] With the root on another branch, the root is unchanged, and the new Cycle Branch HEAD equals `origin/main`. (test)
- [ ] Typecheck and lint are clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
