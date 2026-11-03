---
status: done
mode: hands-off
priority: tracer
blocked_by: []
---
Carry an Appetite through the loop end to end. The Cycle grill (`src/kit/plugin/skills/grill/SKILL.md`) asks for the Cycle's Appetite (elapsed time, Issues, QA rounds) as its first question, uses the default `2 hours, 5 Issues, 2 QA rounds` if the human skips it, and when the frontier is empty commits its `CONTEXT.md` and ADR changes with message `pick: <feature>`. `to-prd` adds an `Appetite:` line under the PRD title, written with `(default)` when the grill used the default. `retro` compares the Cycle against that line: elapsed time from the `pick:` commit to `close:`, the number of Issues, and the number of `qa:` rounds, using the default when the PRD has no Appetite line. Pin each with a test in `tests/test_skills.py`. Use the word Appetite as defined in `CONTEXT.md`.

## Acceptance
- [ ] `grill` asks a Cycle grill's Appetite first and names `2 hours, 5 Issues, 2 QA rounds` as the default
- [ ] `grill` commits `pick: <feature>` when the frontier is empty
- [ ] `to-prd`'s template has an `Appetite:` line, with `(default)` when the default was used
- [ ] `retro` compares elapsed time from `pick:` to `close:`, the Issue count and the `qa:` rounds against the Appetite, defaulting when the PRD has none
- [ ] New tests in `tests/test_skills.py` pin all of the above

## Verify
uv run pytest -q tests/test_skills.py
