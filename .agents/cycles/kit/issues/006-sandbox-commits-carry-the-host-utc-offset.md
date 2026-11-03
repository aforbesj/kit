---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
Sandbox commits are stamped in UTC, so hands-off and hands-on commits read out of order. In `src/kit/cli.py`, the hands-off `docker run` in `agent()` passes `-e TZ=<value>` where the value is the host's current UTC offset as a POSIX TZ string (e.g. `-0500` becomes `<-0500>5`; note POSIX inverts the sign), computed in a small typed helper next to `git_identity`. Git records only the offset, so commit times come out exact. Add a test in `tests/test_cli.py` next to `test_sandbox_run_passes_git_identity`, covering a negative, a positive and a half-hour offset.

## Acceptance
- [ ] The hands-off docker command includes `-e TZ=` with the host's POSIX offset
- [ ] Tests cover negative, positive and half-hour offsets
- [ ] `uv run pyright` and `uv run ruff check` pass

## Verify
uv run pytest -q tests/test_cli.py
