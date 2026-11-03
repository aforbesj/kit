---
name: retro
description: Close a Cycle by moving its lessons to where they last.
disable-model-invocation: true
---

# Retro

Read `progress.txt`, `qa.md` and the Cycle's commits. Ask the human what surprised them. Sort every lesson into one place:

| Lesson | Goes to |
| --- | --- |
| A new or sharper term | `CONTEXT.md` |
| A hard-to-reverse decision | `docs/adr/` |
| A project-specific coding rule | `.agents/standards.md` |
| Scope, Areas, next Features | `CHARTER.md` (only a Charter grill or the retro edits it) |
| An Area whose Features stopped sharing words | `CHARTER.md`: split the Area |
| A process problem with the Kit | Listed in your final message, for the Kit's own Charter |

Remove the finished Feature from `CHARTER.md` and name the next one. If the Area has no next Feature left, tell the human to run `/kit:brainstorm`. Show the edits, apply the approved ones, and commit with message `retro: <feature>`. Then tell the human to run `kit close <area>`.
