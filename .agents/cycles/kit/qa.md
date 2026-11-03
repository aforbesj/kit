# QA: Rank the next Features by how often they're raised

Round 1 of 2. Appetite: 2 hours, 4 Issues, 2 QA rounds. So far: ~1h03m since `pick:`, 5 Issues (005 came from review).

## Done when, measured

| Done when | Result |
| --- | --- |
| Retro counts Raises once per Feature per Cycle, new at 1×, removes finished, sorts with ties to most recent, caps at 6, shows Top 3 / Bottom 3 | Met (`retro/SKILL.md`, tested) |
| Retro no longer says "name the next one" | Met (tested in `test_skills.py` and `test_cli.py`) |
| grill, implement, review, qa append `raised:` to `progress.txt` | 4 of 4 (one shared test) |
| Cycle grill shows Top 3, pick any or new | Met (`grill/SKILL.md` step 2) |
| Charter grill fills Top 3 / Bottom 3, at most 6, with counts | Met |
| Template `CHARTER.md` and README Pick/Close rows describe the ranked list | Met |
| `kit.json` checks pass | pyright 0 errors, ruff clean, pytest 69 passed |
| No SKILL.md body grows by more than 3 lines | grill +2, implement +2, qa +2, review +2, retro +1 |

## See it work

```sh
uv run pyright && uv run ruff check && uv run pytest -q
git diff d4a056e..HEAD -- src README.md
```

## Worth reading

- `src/kit/plugin/skills/retro/SKILL.md`: the ranking rule (last two lines)
- `src/kit/plugin/skills/grill/SKILL.md`: step 2 and the `raised:` line
- `src/kit/template/CHARTER.md`: the format a new Product starts with

## Found by the agent preparing QA

1. The retro breaks ties "to the most recently raised", but `(raised N×)` stores no date, so a later retro can't know which is more recent.
2. The retro's lesson table still says "Scope, Areas, next Features", and `CONTEXT.md` (Charter) and `CLAUDE.md` still say "next Features". These are wording only.
3. The Charter grill runs outside any Cycle, yet the grill sends its `raised:` lines to `.agents/cycles/<area>/progress.txt`. That works, but it creates the file before the Cycle starts.
