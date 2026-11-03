# QA: Every Cycle carries an Appetite

Round 2, past the Appetite of 1. Appetite: 2 hours, 6 Issues, 1 QA round.
So far: 28 min since `pick:` (15:18 to 15:46 -0500), 9 Issues (6 split + 007 from review + 008, 009 from QA round 1), QA round 2.

## Done when

| Done when | Result |
| --- | --- |
| brainstorm: Appetite in step 1, filters before Directions, transcripts, five to eight Directions incl. one with no software, body <= 25 lines | Pass. Body is 15 lines |
| brainstorm last line restates Direction, Appetite, user words; names `/kit:grill` | Pass |
| grill asks Appetite first, names default, commits `pick:` | Pass |
| to-prd has `Appetite:` line, `(default)` when defaulted | Pass |
| to-issues stops and asks past the Appetite | Pass |
| qa asks "a new Issue, or was the PRD wrong?" past the Appetite | Pass. Commits one `qa:` per round (009) |
| retro measures time, Issues, qa: rounds; default when missing | Pass. Time runs from `pick:` to now (008) |
| ADR numbers unique; 0007-cycle-ends-at-merge.md | Pass |
| docker run passes `-e TZ=` host offset | Pass. `TZ=<-0500>5`, proven in docker |
| typecheck, lint, test pass | Pass. pyright 0 errors, ruff clean, 63 passed |

## Round 1 fixes

- 008: `retro` measures from `pick:` to now, and a test refuses `close:`.
- 009: `qa` step 4 makes one `qa: <feature>` commit per round, `--allow-empty` if nothing changed; pinned by a test.

## See it work

    uv run pytest -q
    git diff 597f5c7..HEAD -- src tests

## Worth reading

- `src/kit/plugin/skills/qa/SKILL.md`: steps 2–4
- `src/kit/plugin/skills/retro/SKILL.md`: first paragraph
