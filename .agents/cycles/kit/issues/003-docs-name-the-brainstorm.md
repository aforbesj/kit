---
status: todo
mode: hands-off
priority: polish
blocked_by: [1]
---
Name the Brainstorm in the docs. Change the Phases line in `CLAUDE.md` and `src/kit/template/CLAUDE.md` to match the Phases section of `CONTEXT.md`, which covers an optional Brainstorm then a Charter grill, once at the start and again when an Area runs out of Features, then the Cycle phases. Add a test that keeps both files identical. In `README.md`, name `/kit:brainstorm` as the optional step before the Charter grill in "Start a Product", and as the step after the retro in Close when the Area has no next Feature.

## Acceptance
- [ ] `CLAUDE.md` and `src/kit/template/CLAUDE.md` are identical and their Phases line names Brainstorm
- [ ] `README.md` names `/kit:brainstorm` in "Start a Product" and in the Close step
- [ ] Tests in `tests/` check each line above

## Verify
uv run pyright && uv run ruff check && uv run pytest -q
