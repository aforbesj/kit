# Kit

Plan and build any Product with agents, one Cycle at a time. `CONTEXT.md` defines the terms; `CHARTER.md` says what the Kit is for; `docs/adr/` records why.

## Install once

```bash
git clone <this repo> ~/code/kit && cd ~/code/kit
./setup.sh                # macOS, Linux or WSL2; safe to rerun
```

It installs what is missing (uv, Claude Code, gh, and Docker if you say yes), installs `kit` in editable mode so `git pull` updates it, adds the Claude Code plugin, builds the sandbox, and ends with `kit doctor`. Open a new terminal afterwards so `kit` and `claude` are on PATH.

| System | Docker for hands-off runs |
| --- | --- |
| macOS | OrbStack (setup offers it via Homebrew) or Docker Desktop |
| WSL2 | Docker Desktop for Windows with WSL integration on for your distro |
| Linux | Docker Engine (setup offers get.docker.com) |

No Docker? `./setup.sh --no-docker`, then build with `kit run <area> --local`.

Hands-off runs read `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN`. Run `claude setup-token` and export the token in your shell profile; the macOS keychain login does not reach the sandbox.

Something off? `kit doctor` checks the machine and prints the fix for each gap.

## Start a Product

```bash
kit init my-product      # creates the folder and adds the template; never overwrites a file
cd my-product && claude  # then: /kit:grill  (the Charter grill)
```

Nothing to build yet? Run `/kit:brainstorm` first (optional); it ends by pointing you to `/kit:grill`.

## Run a Cycle

| Phase | Do |
| --- | --- |
| Pick | `kit once <area>`, choose the next Feature, usually from the Area's Top 3 in `CHARTER.md` |
| Research, Prototype | Only if the grill calls for them |
| Plan | `/kit:grill`, then `/kit:to-prd` |
| Split | `/kit:to-issues`, approve the list |
| Build | `kit run <area>` (agents build, validate on Sample data, review) |
| QA | `kit once <area>`, then `/kit:qa` |
| Close | `/kit:retro` (re-ranks the Features by Raises), then `kit close <area>` (or `--abandon` if the PRD was wrong). After the merge, `kit once <area>` starts the next Cycle from the latest `main`, then `/kit:grill` for the next Feature. If the Area has no next Feature, run `/kit:brainstorm` instead, also after the merge |

Sample data goes in `data/<yyyy-mm-dd>-<name>/`, scrubbed by you. Agents read it and write only to `data/out/`.

Areas build in parallel: run `kit run <area>` once per Area. Each gets its own checkout under `.worktrees/` and its own sandbox.

## Change the Kit

The Kit is a Product too. Retro findings about the Kit become its next Cycles. To release, bump the version in `pyproject.toml`, `src/kit/plugin/.claude-plugin/plugin.json`, both copies of `.agents/kit.json` (this repo's and the template's), then run `uv lock`. `tests/test_version.py` fails if any of them differ. Merging to `main` tags `v<version>`.
