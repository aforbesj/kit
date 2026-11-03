---
name: brainstorm
description: Widen a problem into Directions weighed against an Appetite, until the human picks one to grill.
disable-model-invocation: true
---

# Brainstorm

Widen the problem before it is narrowed. Optional: use it when there is nothing to build yet, or an Area has run out of Features.

1. Ask the human for the problem in their own words, who has it, and its Appetite: hours of their time, Issues, QA rounds, money. Read `CHARTER.md` and `CONTEXT.md` if they exist.
2. Ask what rules Directions out before any are named: time, budget, skills, what they refuse to build.
3. Bring evidence: meeting notes or transcripts the human points to (kept under `data/`), Sample data, `progress.txt` from past Cycles, similar products. Find these with the Explore subagent and quote users in their own words.
4. Offer five to eight **Directions**, cheapest to most ambitious, including one that builds no software. Give each one line on the idea and one line on its cost against the Appetite.
5. A Direction bigger than the Appetite is shrunk or dropped; the Appetite stays.
6. Talk it through. Combine, drop or add Directions as the human reacts. Do not design any yet.
7. Stop when the human picks one Direction.

Keep it a conversation. Nothing is saved: no file, and no record of the Directions not chosen.

Last line: restate the chosen Direction, its Appetite and the user words behind it in three lines, then tell the human to run `/kit:grill` in this same session.
