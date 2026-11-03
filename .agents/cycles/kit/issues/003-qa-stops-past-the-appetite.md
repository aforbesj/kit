---
status: todo
mode: hands-off
priority: tracer
blocked_by: [1]
---
`qa` (`src/kit/plugin/skills/qa/SKILL.md`) counts the Cycle's QA rounds (`qa:` commits) against the PRD's `Appetite:` line (or the default when it has none). When a round passes the Appetite, before writing any Issue, it stops and asks the human "a new Issue, or was the PRD wrong?", and records the answer in `progress.txt` for the retro. Nothing is blocked; the existing abandon rule still applies if the PRD was wrong. Pin with a test in `tests/test_skills.py`.

## Acceptance
- [ ] `qa` asks "a new Issue, or was the PRD wrong?" when a round passes the Appetite, before writing Issues
- [ ] The answer goes to `progress.txt`
- [ ] A test in `tests/test_skills.py` pins it

## Verify
uv run pytest -q tests/test_skills.py
