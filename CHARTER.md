# Charter: the Kit

## Problem

Every new product needs the same way to plan and build with agents. Rebuilding it per product wastes time and drifts.

## Users

The Kit Owner, and anyone who forks the Kit as their standard.

## In scope

- The Cycle loop as skills: grill, to-prd, to-issues, implement, review, qa, retro, handoff.
- A `kit` CLI with four commands: init, once, run, close; and `kit doctor` to check the machine.
- One-command setup (`./setup.sh`) on macOS, Linux and WSL2.
- Per-stack standards (Python, TypeScript) and the Product template.

## Out of scope

- Releasing or deploying Products.
- Trackers, dashboards, or anything that needs a server.
- Parallel agents inside one Cycle.

## Areas

- **kit** (owner: Kit Owner): the skills, CLI, setup.sh, standards, template and sandbox. Next, in order:
  1. Close a Cycle and start the next.
  2. Leave a Build running and trust how it stopped.
  3. Start a Product that builds first time.
  4. Sign off QA from recorded results.
  5. Research or Prototype when the grill asks.

Stay tiny: every line must change what an agent does.
