---
status: todo
mode: hands-off
priority: bug
blocked_by: []
---
`retro` (`src/kit/plugin/skills/retro/SKILL.md`) measures elapsed time "from the `pick:` commit to `close:`", but `kit close` runs after the retro, so no `close:` commit exists when it measures. Change it to measure from the `pick:` commit to now (when the retro runs). Update the test in `tests/test_skills.py` that pins the retro's measures so it fails if the retro names `close:` as the end of the clock.

## Acceptance
- [ ] `retro` measures elapsed time from the `pick:` commit to now, not to `close:`
- [ ] A test in `tests/test_skills.py` pins it

## Verify
uv run pytest -q tests/test_skills.py
