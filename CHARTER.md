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
    1. Sign off QA from recorded results: an agent launches what was built (CLI, plugin, app), on a host with Docker, follows `qa.md` and reports before the human judges. (raised 4×, last 2026-11-03)
    2. Start a Product that builds first time, named once a Brainstorm has settled what it is. (raised 2×, last 2026-11-03)
    3. Every `kit run` ends with a Stop reason, including `not started` when Docker or the sandbox fails. (raised 1×, last 2026-11-03)
  - Bottom 3:
    4. `kit status <area>` prints the last Stop reason and the dirty files without starting an agent. (raised 1×, last 2026-11-03)
    5. Fact lookups (grill, Research) run on the cheapest model that is enough, set in `kit.json` models. (raised 1×, last 2026-11-03)
    6. Research or Prototype when the grill asks. (raised 1×, last 2026-11-02)

Stay tiny: every line must change what an agent does.
