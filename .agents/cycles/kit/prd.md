# Brainstorm what to build before a Charter grill

## Problem
The grill only narrows, so it assumes you already know what to build. With nothing to start from, or once an Area runs out of Features, there is no step that widens the problem into Directions first. And the Charter can't grow: only a retro edits it, so a Product whose Features are all built has nowhere to go.

## End state
`/kit:brainstorm` is an optional skill that widens a problem into Directions, each with its cost, through conversation. It uses evidence (Sample data, `progress.txt`, similar products) when that helps. It ends when the human picks one Direction, and it tells them to run `/kit:grill` in the same session. It writes no file and records no rejected Directions. The grill runs as a Charter grill either on an empty Charter or right after a Brainstorm, and that Charter grill may add Features and widen scope. Only a Charter grill or a retro edits `CHARTER.md`, never mid-Cycle (ADR 0006). When a retro leaves an Area with no next Feature, it points the human to `/kit:brainstorm`.

## Done when
- `src/kit/plugin/skills/brainstorm/SKILL.md` exists with `name: brainstorm` and `disable-model-invocation: true` (test)
- The brainstorm skill names `/kit:grill` as its last step and has no instruction to write a file (test)
- The brainstorm skill's body is 25 lines or fewer (test)
- The grill skill names `/kit:brainstorm` for an empty Charter and runs a Charter grill on a filled Charter after a Brainstorm (test)
- The retro skill names `/kit:brainstorm` for an Area with no next Feature and still contains "Remove the finished Feature from `CHARTER.md` and name the next one" (test)
- The template `CHARTER.md` no longer says "only a retro edits it" and names the Charter grill and the retro (test)
- `CLAUDE.md` and `src/kit/template/CLAUDE.md` stay identical and their Phases line names Brainstorm (test)
- `README.md` names `/kit:brainstorm` in "Start a Product" and in the Close step (test)
- `uv run pyright`, `uv run ruff check` and `uv run pytest -q` all pass (test)

## Out of scope
- Automatic `/kit:handoff` (a hook that counts tokens).
- Defining Research and Prototype (Feature 5).
- CLI changes, including the `kit init` and `kit close` "Next" messages.
- Any file the Brainstorm writes, and any record of rejected Directions.

## What changes
- New: `src/kit/plugin/skills/brainstorm/SKILL.md`
- `src/kit/plugin/skills/grill/SKILL.md`, `src/kit/plugin/skills/retro/SKILL.md`
- `src/kit/template/CHARTER.md`, `src/kit/template/CLAUDE.md`, `CLAUDE.md`, `README.md`
- `tests/` (text checks for the above)
- Already done in the grill: `CONTEXT.md`, `CHARTER.md`, `docs/adr/0006-charter-changes-between-cycles.md`
- Sample data: none
