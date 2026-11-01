---
name: qa
description: Prepare the human's QA of a built Cycle and record what they find.
disable-model-invocation: true
---

# QA

The human judges; you prepare and record.

1. Write `.agents/cycles/<area>/qa.md`: each Done when line with its measured result from `progress.txt`, the commands to see the Feature work, and the files most worth reading in the diff.
2. Walk the human through it. For each problem they report, write a new Issue (`priority: bug`).
3. If the human finds the PRD itself was wrong, stop: the Cycle is abandoned. Tell them to run `/kit:retro`, then `kit close <area> --abandon`.

**Done when** the human signs off (then: `/kit:retro`, then `kit close <area>`) or new Issues exist (then: `kit run <area>`).
