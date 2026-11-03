# QA: Rank the next Features by how often they're raised

Round 2 of 2. Appetite: 2 hours, 4 Issues, 2 QA rounds. So far: ~1h08m since `pick:`, 8 Issues (005 from review; 006–008 from QA round 1). A third round would pass the Appetite.

## Done when, measured

| Done when | Result |
| --- | --- |
| Retro counts Raises once per Feature per Cycle, new at 1×, removes finished, sorts with ties to most recent, caps at 6, shows Top 3 / Bottom 3 | Met; ties now go to the later `last` date (006) |
| Retro no longer says "name the next one" | Met (tested) |
| grill, implement, review, qa append `raised:` to `progress.txt` | 4 of 4; the grill does this only in a Cycle grill (008) |
| Cycle grill shows Top 3, pick any or new | Met |
| Charter grill fills Top 3 / Bottom 3, at most 6, with counts | Met, format `(raised N×, last YYYY-MM-DD)` |
| Template `CHARTER.md` and README Pick/Close rows describe the ranked list | Met |
| `kit.json` checks pass | pyright 0 errors, ruff clean, pytest 72 passed |
| No SKILL.md body grows by more than 3 lines | grill +2, implement +2, qa +2, review +2, retro +1 |

## Round 1 findings

| Finding | Issue | Now |
| --- | --- | --- |
| Tie-break had no date | 006 | `(raised N×, last YYYY-MM-DD)`; retro sets `last` to today, ties to the later `last` |
| "next Features" wording | 007 | Retro row, `CONTEXT.md`, both `CLAUDE.md` say "ranked Features"; `git grep "next Features"` in src, CONTEXT, CLAUDE, README finds nothing |
| Charter grill Raises went to a Cycle file | 008 | Cycle grill → `progress.txt`; Charter grill → `CHARTER.md` at 1× |

## See it work

```sh
uv run pyright && uv run ruff check && uv run pytest -q
git diff 99f03ae..HEAD -- src CONTEXT.md CLAUDE.md
```

## Worth reading

- `src/kit/plugin/skills/retro/SKILL.md`: the ranking rule (last two lines)
- `src/kit/plugin/skills/grill/SKILL.md`: the Cycle grill / Charter grill split on `raised:`
- `src/kit/template/CHARTER.md`: the format

## Left for the retro

- This Kit's own `CHARTER.md` still uses the old ordered list. The retro seeds the counts with dates, renames the Feature, and removes it.
