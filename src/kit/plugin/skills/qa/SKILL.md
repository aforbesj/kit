---
name: qa
description: Prepare the human's QA of a built Cycle and record what they find.
disable-model-invocation: true
---

# QA

The human judges; you prepare and record.

1. Write `.agents/cycles/<area>/qa.md`: each Done when line with its measured result from `progress.txt`, the commands to see the Feature work, and the files most worth reading in the diff.
2. Walk the human through it. Count this Cycle's QA rounds (`qa:` commits, this one included) against the PRD's Appetite (the default `2 hours, 5 Issues, 2 QA rounds` if it has none). If this round passes the Appetite, stop before writing any Issue and ask: "a new Issue, or was the PRD wrong?" Record the answer in `progress.txt` for the retro.
3. For each problem they report (and the answer is a new Issue), write a new Issue (`priority: bug`). Nothing is blocked.
4. If the human finds the PRD itself was wrong, stop: the Cycle is abandoned. Tell them to run `/kit:retro`, then `kit close <area> --abandon`.

**Done when** the human signs off (then: `/kit:retro`, then `kit close <area>`) or new Issues exist (then: `kit run <area>`).
