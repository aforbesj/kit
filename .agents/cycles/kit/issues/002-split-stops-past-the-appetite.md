---
status: done
mode: hands-off
priority: tracer
blocked_by: [1]
---
`to-issues` (`src/kit/plugin/skills/to-issues/SKILL.md`) compares the drafted list against the PRD's `Appetite:` line (or the default `2 hours, 5 Issues, 2 QA rounds` when it has none). When the split has more Issues than the Appetite, it says so and asks the human "shrink the split, or was the grill too big?" before writing or committing any Issue. Pin with a test in `tests/test_skills.py`.

## Acceptance
- [ ] `to-issues` names the Appetite and stops to ask before committing when the Issue count passes it
- [ ] A test in `tests/test_skills.py` pins it

## Verify
uv run pytest -q tests/test_skills.py
