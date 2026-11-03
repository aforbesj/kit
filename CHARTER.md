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

- **kit** (owner: Kit Owner): the skills, CLI, setup.sh, standards, template and sandbox. Next, in order:
  1. Leave a Build running and trust how it stopped: no staged-but-uncommitted work, `kit doctor` warns when the installed `kit` is older than the Product's, and the sandbox and the host don't rebuild each other's `.venv`.
  2. Start a Product that builds first time, named once a Brainstorm has settled what it is.
  3. Sign off QA from recorded results: an agent launches what was built (CLI, plugin, app), follows `qa.md` and reports before the human judges.
  4. Research or Prototype when the grill asks.

Stay tiny: every line must change what an agent does.
