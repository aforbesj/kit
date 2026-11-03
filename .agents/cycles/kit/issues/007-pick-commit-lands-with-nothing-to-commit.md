---
status: done
mode: hands-off
priority: bug
blocked_by: []
---
The Cycle grill (`src/kit/plugin/skills/grill/SKILL.md`) says to "commit the `CONTEXT.md` and ADR changes with message `pick: <feature>`". Many Cycle grills settle no new term and write no ADR, so there is nothing to commit: `git commit` fails, no `pick:` commit exists, and the retro has no start for the Cycle's clock. The PRD's Done when asks that the grill commits `pick: <feature>` every time the frontier is empty. Make the commit happen even with no changes (`git commit --allow-empty -m "pick: <feature>"`, staging `CONTEXT.md` and `docs/adr/` when they changed), and pin it with a test in `tests/test_skills.py`.

## Acceptance
- [ ] Failing test first: `test_grill_pick_commit_lands_with_no_changes` asserts the grill skill names `--allow-empty` on the `pick: <feature>` commit
- [ ] The grill skill makes the `pick:` commit whether or not `CONTEXT.md` or `docs/adr/` changed
- [ ] `uv run pyright`, `uv run ruff check` and `uv run pytest -q` pass

## Verify
uv run pytest -q tests/test_skills.py
