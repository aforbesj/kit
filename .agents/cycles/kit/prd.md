# Every Cycle carries an Appetite

Appetite: 2 hours, 6 Issues, 1 QA round

## Problem
Nothing in the loop says what a Cycle is worth, so nothing notices when it runs past that. The Brainstorm Cycle took about 1h45, 7 Issues and 3 QA rounds; rounds 2 and 3 changed the concept rather than finding bugs, and the "was the PRD wrong?" question never fired. The Brainstorm also names Directions before their limits are known. Two housekeeping faults sit alongside: two ADRs are numbered 0001, and sandbox commits are stamped in UTC so hands-off and hands-on commits read out of order.

## End state
Every Cycle carries an Appetite (elapsed time, Issues, QA rounds), set first by the Cycle grill or defaulted to `2 hours, 5 Issues, 2 QA rounds (default)`. The PRD records it; Split and QA stop and ask when they pass it; the retro measures the Cycle against it, with time counted from the `pick:` commit, which the Cycle grill now makes. The Brainstorm asks for the Appetite and the filters before offering five to eight Directions. ADR numbers are unique, and sandbox commits carry the host's UTC offset.

## Done when
- `brainstorm` asks for the Appetite in step 1, asks for what rules Directions out before any are named, names meeting notes or transcripts as evidence, and asks for five to eight Directions including one that builds no software; its body stays at or under 25 lines (test)
- `brainstorm`'s last line restates the chosen Direction, its Appetite and the user words behind it, and names `/kit:grill` (test)
- `grill` asks a Cycle grill's Appetite as its first question, names the default `2 hours, 5 Issues, 2 QA rounds`, and commits `pick: <feature>` when the frontier is empty (test)
- `to-prd`'s template has an `Appetite:` line, written with `(default)` when the grill used the default (test)
- `to-issues` stops and asks before committing when the split has more Issues than the Appetite (test)
- `qa` stops and asks "a new Issue, or was the PRD wrong?" when a round passes the Appetite, before writing Issues (test)
- `retro` compares elapsed time from `pick:` to `close:`, the Issue count and the `qa:` rounds against the PRD's Appetite, using the default when the PRD has none (test)
- `docs/adr/` has no two files with the same number; `0001-cycle-ends-at-merge.md` is now `0007-cycle-ends-at-merge.md` (test)
- The hands-off `docker run` command passes `-e TZ=` set to the host's current UTC offset (test)
- `typecheck`, `lint` and `test` from `.agents/kit.json` all pass (test)

## Out of scope
- Bets and a candidates list for the Charter's Features: the retro adds it as the next Feature.
- Appetite on Charter Features.
- Recording hands-on time apart from wall-clock time.
- Any new CLI command or measurement code: the retro counts from git.

## What changes
- `src/kit/plugin/skills/{brainstorm,grill,to-prd,to-issues,qa,retro}/SKILL.md`
- `src/kit/cli.py` (`agent`: TZ flag)
- `docs/adr/0001-cycle-ends-at-merge.md` → `docs/adr/0007-cycle-ends-at-merge.md`
- `tests/test_skills.py`, `tests/test_cli.py`
- Sample data: none
