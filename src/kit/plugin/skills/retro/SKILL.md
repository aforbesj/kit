---
name: retro
description: Close a Cycle by moving its lessons to where they last.
disable-model-invocation: true
---

# Retro

Read `progress.txt`, `qa.md` and the Cycle's commits. Measure the Cycle against the PRD's Appetite: elapsed time from the `pick:` commit to now (`kit close` has not run yet), the number of Issues, and the number of `qa:` rounds (use `2 hours, 5 Issues, 2 QA rounds` if the PRD has no Appetite line). Say where it ran past. Ask the human what surprised them. Sort every lesson into one place:

| Lesson | Goes to |
| --- | --- |
| A new or sharper term | `CONTEXT.md` |
| A hard-to-reverse decision | `docs/adr/` |
| A project-specific coding rule | `.agents/standards.md` |
| Scope, Areas, next Features | `CHARTER.md` (only a Charter grill or the retro edits it) |
| An Area whose Features stopped sharing words | `CHARTER.md`: split the Area |
| A process problem with the Kit | Listed in your final message, for the Kit's own Charter |

Then re-rank the Area's Features in `CHARTER.md`. Match each of the `raised:` lines in `progress.txt` against the Features: a match bumps that Feature's `(raised N×)` once per Feature per Cycle, and a new idea joins at 1×. Remove the finished Feature, sort by count with ties to the most recently raised, cap the list at 6 (drop the lowest), and show it as a Top 3 and a Bottom 3.
Show the edits, apply the approved ones, and commit with message `retro: <feature>`. Then tell the human to run `kit close <area>`. If the Area has no Feature left, add that after the merge, from the latest `main`, they run `/kit:brainstorm`.
