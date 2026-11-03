---
status: todo
mode: hands-off
priority: tracer
blocked_by: [4]
---
When a remote exists, `kit close <area> --abandon` pushes the `abandoned/...` tag to `origin` and deletes `cycle/<area>` from `origin` as well as locally. With no remote, it keeps the tag locally and returns 0.

## Acceptance
- [ ] With a remote, `--abandon` leaves the tag on the remote and `cycle/<area>` gone from the remote. (test)
- [ ] With no remote, `--abandon` returns 0 and keeps the tag locally. (test)
- [ ] Typecheck and lint are clean.

## Verify
uv run pytest -q && uv run pyright && uv run ruff check
