---
status: done
mode: hands-off
priority: polish
blocked_by: [1]
---
Rewrite `src/kit/plugin/skills/brainstorm/SKILL.md` so a Brainstorm weighs Directions against an Appetite. Step 1 asks for the problem in the human's words, who has it, and its Appetite (hours of their time, Issues, QA rounds, money). Step 2 asks what rules Directions out before any are named: time, budget, skills, what they refuse to build. Evidence names meeting notes or transcripts the human points to (kept under `data/`), Sample data, `progress.txt` from past Cycles and similar products, found with the Explore subagent, quoting users in their own words. Offer five to eight Directions, cheapest to most ambitious, including one that builds no software, each with one line on its cost against the Appetite. A Direction bigger than the Appetite is shrunk or dropped; the Appetite stays. Nothing is saved. Last line: restate the chosen Direction, its Appetite and the user words behind it in three lines, then tell the human to run `/kit:grill` in this same session. Keep existing tests passing (body at or under 25 lines, last line names `/kit:grill`, no file written) and add tests for the new rules.

## Acceptance
- [ ] Step 1 asks for the Appetite; filters are asked before any Direction is named
- [ ] Meeting notes or transcripts are named as evidence
- [ ] Five to eight Directions, one that builds no software
- [ ] Last line restates Direction, Appetite and user words and names `/kit:grill`
- [ ] Body is at or under 25 lines; tests in `tests/test_skills.py` pin the new rules

## Verify
uv run pytest -q tests/test_skills.py
