---
name: grill
description: Interview the human until you share one design; record terms and decisions as they land.
disable-model-invocation: true
---

# Grill

Reach a shared design with the human by asking, never by assuming.

1. Read `CHARTER.md`, `CONTEXT.md` and `docs/adr/`. If `CHARTER.md` is still the empty template and no Brainstorm came first, offer `/kit:brainstorm` before grilling; the human may decline. If it is the empty template, or the human has just finished a Brainstorm in this session (even on a filled Charter), this is the **Charter grill**; otherwise it is a **Cycle grill** for the Area and Feature the human names.
2. For a Cycle grill, first show the Area's Top 3 from `CHARTER.md`; the human picks any Feature on the list or something new. Then ask the **Appetite**: elapsed time, Issues and QA rounds this Feature is worth. If the human skips it, use the default `2 hours, 5 Issues, 2 QA rounds` and say so.
3. Map the decisions as a tree. The **frontier** is every decision whose prerequisites are settled.
4. Ask the frontier in rounds. Number each question, keep it to a few lines, and give your recommended answer after `➡️`. Wait for answers.
5. Look up facts yourself (code, files, `--help`) with the Explore subagent. Put only decisions to the human.
6. As each answer lands:
   - A term is settled: add it to `CONTEXT.md` (term, one-line definition, `_Avoid_:` synonyms). Vocabulary only.
   - A decision is hard to reverse, surprising, and a real trade-off: write `docs/adr/NNNN-slug.md` in one paragraph.
   - A term clashes with `CONTEXT.md`, or a word is fuzzy: call it out and propose one precise term.
7. Recompute the frontier and repeat until it is empty.

When an idea for a Feature comes up, append `raised: <idea>` to `.agents/cycles/<area>/progress.txt` (create it if missing).

**Done when** the frontier is empty and the human confirms the shared understanding.

Then, for a Charter grill, fill `CHARTER.md`: Problem, Users, In scope, Out of scope, Areas (each with an owner, a Top 3 and a Bottom 3: at most 6 Features, each with `(raised N×, last YYYY-MM-DD)`). One page. For a Cycle grill, stage `CONTEXT.md` and `docs/adr/` if they changed, then always commit with message `pick: <feature>` using `git commit --allow-empty`, even when nothing changed (the start of the Cycle's clock), decide whether Research or Prototype is needed, then tell the human to run `/kit:to-prd`.

A Charter grill run after a Brainstorm may add Features and widen scope on a filled Charter. Only a Charter grill or a retro edits `CHARTER.md`, never mid-Cycle.
