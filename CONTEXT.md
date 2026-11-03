# Agentic Cycle System

One repeatable way to plan and build any product with agents. From largest to smallest: Product, Area, Feature, Issue.

## Language

**Product**: One repo: one problem, one set of users, one name.
_Avoid_: project, codebase, app

**Charter**: The Product's one page: the problem, what's in and out of scope, its Areas and their next Features.
_Avoid_: vision, roadmap

**Area**: A group of Features that share the same words and data. Every Product starts as one Area; a retro splits it when its Features stop sharing them.
_Avoid_: context, module, domain

**Feature**: Something a user can do with the Product. Belongs to one Area.
_Avoid_: capability, function, epic

**Cycle**: Building or changing one Feature, from Pick to Close. Ends when its Cycle Branch merges. One per Area at a time.
_Avoid_: sprint, iteration

**Cycle Branch**: The Area's one branch for the running Cycle, `cycle/<area>`, merged once after QA by a merge commit. A squash merge leaves the Cycle open.
_Avoid_: feature branch, worktree

**PRD**: The Cycle's end state and its measurable Done when targets. Locked during the Cycle, deleted after.
_Avoid_: spec, plan

**Issue**: One thin, end-to-end piece of a Feature, built in one pass.
_Avoid_: ticket, story, task

**Sample data**: Real data copied out and scrubbed by a person before any agent sees it, kept in a dated folder under the repo's git-ignored data folder. Agents only read it.
_Avoid_: test data, fixtures, prod copy

**Validation**: Running a Feature on Sample data against the PRD's Done when targets. Comes after test cases and before QA.
_Avoid_: score, eval, UAT

**Gate**: A check work must pass to move on.
_Avoid_: guardrail, policy

**Hands-on**: You steer the agent.
_Avoid_: HITL, interactive

**Hands-off**: The agent works alone.
_Avoid_: AFK, autonomous

**Kit**: The skills and CLI that run all of this, the same in every Product.
_Avoid_: framework, toolkit

## Phases

A Product begins with one Charter grill. Each Cycle then runs: Pick, Research, Prototype, Plan, Split, Build, QA, Close. Research and Prototype run only when the grill calls for them.
