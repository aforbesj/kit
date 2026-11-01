# Charter: the Kit

## Problem

Every new product needs the same way to plan and build with agents. Rebuilding it per product wastes time and drifts.

## Users

The Kit Owner, and anyone who forks the Kit as their standard.

## In scope

- The Cycle loop as skills: grill, to-prd, to-issues, implement, review, qa, retro, handoff.
- A `kit` CLI with four commands: init, once, run, close.
- Per-stack standards (Python, TypeScript) and the Product template.

## Out of scope

- Releasing or deploying Products.
- Trackers, dashboards, or anything that needs a server.
- Parallel agents inside one Cycle.

## Areas

- **Loop** (owner: Kit Owner): the skills. Next: tune Issue size after the first real Cycle.
- **CLI** (owner: Kit Owner): init, once, run, close. Next: none until a retro asks.

Stay tiny: every line must change what an agent does.
