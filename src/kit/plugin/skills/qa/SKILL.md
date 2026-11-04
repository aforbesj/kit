---
name: qa
description: Prepare the human's QA of a built Cycle and record what they find.
disable-model-invocation: true
---

# QA

The human judges; you prepare and record.

1. Read `.agents/cycles/<area>/qa.md`, the results `kit run` recorded for each QA step (the step, what you should see, exit code, duration, output tail, log path). Walk the human through each result against what they should see. Don't write or edit it.
2. Read `launch` in `.agents/kit.json`. If it is empty, ask the human once for the one command that opens the Product and write it into `kit.json`. Then show the command and run `launch` on the host, unscrubbed, and leave the Product open for the human's **Hunt**: their own exploring for bugs and ideas. Anything you start ends with your tool call, so if `launch` is interactive (a `claude` session, a shell, a TUI), don't run it: show the exact command and tell the human to run it from the worktree root in a new terminal. Start only a background `launch` (a server) yourself, and say how to stop it (for example the kill command for its process).
3. Count this Cycle's QA rounds (`qa:` commits, this one included) against the PRD's Appetite (the default `2 hours, 5 Issues, 2 QA rounds` if it has none). If this round passes the Appetite, stop before writing any Issue and ask: "a new Issue, or was the PRD wrong?" Record the answer in `progress.txt` for the retro.
4. For each bug the Hunt turns up (and the answer is a new Issue), write a new Issue (`priority: bug`). Nothing is blocked. Feature ideas become `raised: <idea>` lines in `progress.txt`.
5. Commit once per round, after `kit.json` (if `launch` changed) and any new Issues are written: `git commit -m "qa: <feature>"` (add `--allow-empty` if nothing changed), so each round leaves exactly one `qa:` commit for the breaker and the retro to count.
6. If the human finds the PRD itself was wrong, stop: the Cycle is abandoned. Tell them to run `/kit:retro`, then `kit close <area> --abandon`.

When an idea for a Feature comes up, append `raised: <idea>` to `progress.txt`.

**Done when** the human signs off (then: `/kit:retro`, then `kit close <area>`) or new Issues exist (then: `kit run <area>`).
