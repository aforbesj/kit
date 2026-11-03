# QA: Every Cycle carries an Appetite

Round 1 of an Appetite of 1. Appetite: 2 hours, 6 Issues, 1 QA round.
So far: 23 min since `pick:` (15:18 to 15:41 -0500), 7 Issues (006 + review-found 007), this QA round.

## Done when

| Done when | Result |
| --- | --- |
| brainstorm: Appetite in step 1, filters before Directions, transcripts, five to eight Directions incl. one with no software, body <= 25 lines | Pass. Body is 15 lines; 4 tests |
| brainstorm last line restates Direction, Appetite, user words; names `/kit:grill` | Pass |
| grill asks Appetite first, names default, commits `pick:` | Pass. `--allow-empty` added by 007 |
| to-prd has `Appetite:` line, `(default)` when defaulted | Pass |
| to-issues stops and asks past the Appetite | Pass |
| qa asks "a new Issue, or was the PRD wrong?" past the Appetite | Pass |
| retro measures pick to close, Issues, qa: rounds; default when missing | Pass as written; see finding 2 |
| ADR numbers unique; 0007-cycle-ends-at-merge.md | Pass |
| docker run passes `-e TZ=` host offset | Pass. Host gives `TZ=<-0500>5`; `docker run -e 'TZ=<-0500>5' alpine date` prints -0500 |
| typecheck, lint, test pass | Pass. pyright 0 errors, ruff clean, 62 passed |

## Findings for the human

1. The hands-off commits on this branch still read +0000. The Build ran the installed `kit-cycle v0.2.0` (a non-editable uv tool), so it used the old code. The fix is only proven live in the next Cycle, after a reinstall. This is Charter Feature 1 (`kit doctor` warns about an old installed `kit`).
2. The retro measures time to the `close:` commit, but `kit close` runs after the retro, so that commit doesn't exist yet when the retro measures.
3. The QA breaker counts `qa:` commits, but no skill says to make one. This round's commit follows convention only.
4. Issues went past the Appetite (7 against 6) through a review-found bug, and nothing asked the question. The breaker only fires at Split.

## See it work

    uv run pytest -q
    uv run python -c "from pathlib import Path; from kit import cli; print([a for a in cli.agent({}, Path('.'), Path('.'), 'sonnet', 'go', hands_off=True, local=False) if a.startswith('TZ=')])"
    git diff 5957e60..HEAD -- src/kit/plugin/skills

## Worth reading

- `src/kit/plugin/skills/qa/SKILL.md`: steps 2–3
- `src/kit/plugin/skills/grill/SKILL.md`: step 2 and the closing paragraph
- `src/kit/cli.py`: `posix_tz`
