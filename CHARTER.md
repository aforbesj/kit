# Charter: the Kit

## Problem

Every new product needs the same way to plan and build with agents. Rebuilding it per product wastes time and drifts.

## Users

The Kit Owner, and anyone who forks the Kit as their standard.

## In scope

- Brainstorm, then the Cycle loop as skills: grill, to-prd, to-issues, implement, review, qa, retro, handoff.
- A `kit` CLI with four commands: init, once, run, close; and `kit doctor` to check the machine.
- One-command setup (`./setup.sh`) on macOS, Linux and WSL2.
- Per-stack standards (Python, TypeScript) and the Product template.

## Out of scope

- Releasing or deploying Products.
- Trackers, dashboards, or anything that needs a server.
- Parallel agents inside one Cycle.

## Areas

- **kit** (owner: Kit Owner): the skills, CLI, setup.sh, standards, template and sandbox.
  - Top 3:
    1. Start a Product that builds first time, named once a Brainstorm has settled what it is. (raised 2×, last 2026-11-03)
    2. A Kit Cycle runs end to end on its own working copy: `kit run` uses the new CLI after it changes, and grill and qa sessions load the worktree's plugin. (raised 1×, last 2026-11-03)
    3. Review measures QA steps without overwriting the real `qa.md`. (raised 1×, last 2026-11-03)
  - Bottom 3:
    4. Every `kit run` ends with a Stop reason, including `not started` when Docker or the sandbox fails. (raised 1×, last 2026-11-03)
    5. Ignore lines scoped to `.agents/cycles/*/qa.md` and `qa-logs/`, so a Product's own `qa.md` isn't hidden. (raised 1×, last 2026-11-03)
    6. `kit status <area>` prints the last Stop reason and the dirty files without starting an agent. (raised 1×, last 2026-11-03)

Stay tiny: every line must change what an agent does.
