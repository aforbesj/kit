---
name: brainstorm
description: Widen a problem into Directions, each with its cost, until the human picks one to grill.
disable-model-invocation: true
---

# Brainstorm

Widen the problem before it is narrowed. Optional: use it when there is nothing to build yet, or an Area has run out of Features.

1. Ask the human for the problem in their own words, and read `CHARTER.md` and `CONTEXT.md` if they exist.
2. Bring evidence when it helps: Sample data in `data/`, `progress.txt` from past Cycles, similar products. Look these up yourself with the Explore subagent.
3. Offer many **Directions**, broad and different from each other. For each, give one line on the idea and one line on its cost (effort, risk, what it rules out).
4. Talk it through. Combine, drop or add Directions as the human reacts. Do not design any of them yet.
5. Stop when the human picks one Direction.

Keep it a conversation. Nothing is saved: no file, and no record of the Directions not chosen.

Last step: tell the human to run `/kit:grill` in this same session, so the chosen Direction carries into the Charter grill.
