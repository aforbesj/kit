# Kit

Plan and build any Product with agents, one Cycle at a time. `CONTEXT.md` defines the terms; `CHARTER.md` says what the Kit is for; `docs/adr/` records why.

## Install once

```bash
uv tool install .                         # the kit CLI
docker build -t kit-sandbox sandbox/      # sandbox for hands-off runs
```

In Claude Code:

```
/plugin marketplace add /path/to/kit
/plugin install kit@kit
```

Hands-off runs read `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`).

## Start a Product

```bash
mkdir my-product && cd my-product
kit init                 # adds the template; never overwrites a file
claude                   # then: /kit:grill  (the Charter grill)
```

## Run a Cycle

| Phase | Do |
| --- | --- |
| Pick | `kit once <area>`, choose the next Feature from `CHARTER.md` |
| Research, Prototype | Only if the grill calls for them |
| Plan | `/kit:grill`, then `/kit:to-prd` |
| Split | `/kit:to-issues`, approve the list |
| Build | `kit run <area>` (agents build, validate on Sample data, review) |
| QA | `kit once <area>`, then `/kit:qa` |
| Close | `/kit:retro`, then `kit close <area>` (or `--abandon` if the PRD was wrong) |

Sample data goes in `data/<yyyy-mm-dd>-<name>/`, scrubbed by you. Agents read it and write only to `data/out/`.

Areas build in parallel: run `kit run <area>` once per Area. Each gets its own checkout under `.worktrees/` and its own sandbox.

## Change the Kit

The Kit is a Product too. Retro findings about the Kit become its next Cycles. Bump the version in `pyproject.toml` and `src/kit/plugin/.claude-plugin/plugin.json` together.
