# Agentic Cycle System

One repeatable way to plan and build any product with agents. From largest to smallest: Product, Area, Feature, Issue.

## Language

**Product**: One repo: one problem, one set of users, one name.
_Avoid_: project, codebase, app

**Charter**: The Product's one page: the problem, what's in and out of scope, its Areas and their ranked Features. Only a Charter grill or a retro edits it, never mid-Cycle.
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

**Brainstorm**: Widening a problem into many directions until the human chooses one to grill. Optional; runs outside any Cycle, from the latest `main`, before a Charter grill. Rejects nothing on record.
_Avoid_: ideation, discovery, exploration

**Direction**: A broad way to address the problem, with its cost; not yet a design. A Brainstorm widens into many; the human picks one to grill.
_Avoid_: option, solution, idea

**Appetite**: What a Feature or Direction is worth before it is designed, in time, size and QA rounds. A Brainstorm sets it for a Direction, the Cycle grill for a Feature (a default if skipped). The retro measures the Cycle against it. Not a deadline.
_Avoid_: estimate, budget, deadline

**Raise**: An idea for a Feature coming up during a Cycle. Counted at most once per Cycle; Raises rank an Area's Features.
_Avoid_: mention, vote

**Gate**: A check work must pass to move on.
_Avoid_: guardrail, policy

**Hands-on**: You steer the agent.
_Avoid_: HITL, interactive

**Hands-off**: The agent works alone.
_Avoid_: AFK, autonomous

**Kit**: The skills and CLI that run all of this, the same in every Product.
_Avoid_: framework, toolkit

## Phases

The Charter is shaped by an optional Brainstorm, then a Charter grill: once at the start, and again whenever an Area runs out of Features. Each Cycle builds one Feature: Pick, Research, Prototype, Plan, Split, Build, QA, Close. Research and Prototype run only when the grill calls for them.
