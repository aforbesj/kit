# Rank the next Features by how often they're raised

Appetite: 2 hours, 4 Issues, 2 QA rounds

## Problem
Each Area keeps a hand-ordered list of next Features that nobody re-ranks and that can grow without limit. Ideas that come up mid-Cycle have nowhere to go, because the Charter cannot change during a Cycle, so they get lost. An Area that runs out of Features forces a Brainstorm even when past Cycles raised plenty of ideas.

## End state
Each Area in `CHARTER.md` has one Features list of at most 6, shown as a Top 3 and a Bottom 3. Each line carries a count, e.g. `(raised 2×)`. The list is sorted by count, and ties go to the most recently raised. When an idea for a Feature comes up during a Cycle, the skill in use appends a `raised:` line to the Cycle's `progress.txt`. At the retro, the agent matches each `raised:` line against the list: a match bumps that Feature once per Cycle, and a new idea joins at 1×. The retro also removes the finished Feature, drops the lowest when the list passes 6, and shows the new tiers. At the next grill the human picks the next Feature, usually from the Top 3, though any Feature or something new is allowed. Only the retro or a Charter grill edits the Charter (ADR 0006 unchanged; ADR 0008 records the ranking).

## Done when
- The retro skill tells the agent to count Raises from `progress.txt` once per Feature per Cycle, add new ideas at 1×, remove the finished Feature, sort by count with ties to the most recent, cap at 6 and show the Top 3 and Bottom 3 (yes/no) (test)
- The retro skill no longer says "name the next one" (yes/no) (test)
- The grill, implement, review and qa skills each tell the agent to append a `raised:` line to `progress.txt` when an idea for a Feature comes up (4 of 4) (test)
- The Cycle grill shows the Area's Top 3 and lets the human pick any Feature or something new (yes/no) (test)
- The Charter grill fills each Area with a Top 3 and a Bottom 3, at most 6 Features with counts (yes/no) (test)
- The template `CHARTER.md` and the README Pick and Close rows describe the Top 3 / Bottom 3 list ranked by Raises (yes/no) (test)
- `kit.json` checks pass with no failing tests (yes/no) (test)
- Each skill touched stays within the length check in `tests/test_skills.py`, and no SKILL.md body grows by more than 3 lines (yes/no) (test)

## Out of scope
- Editing this Kit's own `CHARTER.md`: the counts are seeded and the Feature renamed at this Cycle's retro, not during the Build.
- Any CLI change: `kit` does not parse the Charter (ADR 0007).
- Recording Raises during a Brainstorm (it writes no file).
- Keeping any record of Features that dropped off the list.

## What changes
- `src/kit/plugin/skills/retro/SKILL.md`, `grill/SKILL.md`, `implement/SKILL.md`, `review/SKILL.md`, `qa/SKILL.md`
- `src/kit/template/CHARTER.md`, `README.md`
- `tests/test_skills.py`
- Sample data: none
