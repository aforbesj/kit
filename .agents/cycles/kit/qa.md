# QA: Brainstorm what to build before a Charter grill

## Done when

| Done when | Result (from `progress.txt`, re-run at QA) |
|---|---|
| `brainstorm/SKILL.md` exists, `name: brainstorm`, `disable-model-invocation: true` | Met (001; test in `tests/test_skills.py`) |
| Brainstorm names `/kit:grill` as last step, no instruction to write a file | Met (001) |
| Brainstorm body is 25 lines or fewer | Met (001; body is 15 lines) |
| Grill names `/kit:brainstorm` for an empty Charter; Charter grill on a filled Charter after a Brainstorm | Met (001) |
| Retro names `/kit:brainstorm` for an Area with no next Feature; keeps "Remove the finished Feature..." | Met (002) |
| Template `CHARTER.md` drops "only a retro edits it", names Charter grill and retro | Met (002) |
| Both `CLAUDE.md` files identical; Phases line names Brainstorm | Met (003) |
| `README.md` names `/kit:brainstorm` in Start a Product and Close | Met (003) |
| pyright, ruff check, pytest pass | Met: pyright 0 errors, ruff clean, pytest 39 passed (re-run at QA) |

## See it work

```sh
uv run pytest -q tests/test_skills.py
diff CLAUDE.md src/kit/template/CLAUDE.md && echo identical
cat src/kit/plugin/skills/brainstorm/SKILL.md
```

Then in a scratch Product (`kit init /tmp/try && cd /tmp/try && claude`):
1. `/kit:grill` on the empty Charter: it should offer `/kit:brainstorm` first.
2. `/kit:brainstorm`: Directions with costs, no file written, ends pointing to `/kit:grill`.
3. `/kit:grill` in the same session: runs as a Charter grill.

## Worth reading in the diff

- `src/kit/plugin/skills/brainstorm/SKILL.md`: the whole new skill.
- `src/kit/plugin/skills/grill/SKILL.md` step 1: the Charter-vs-Cycle grill rule is now one long sentence.
- `src/kit/plugin/skills/retro/SKILL.md` last paragraph, beside the README Close row: the order of `/kit:brainstorm` and `kit close` differs (retro says brainstorm then close; README says "after the retro", ambiguous about the merge).

## Review notes carried from Build (not failures)

- `CHARTER.md` "In scope" skill list and `plugin.json` description omit brainstorm.
- Where the Brainstorm belongs relative to `kit close` (on the Cycle branch, or after the merge on `main`).

## Findings

Human tried it with the branch's plugin (`claude --plugin-dir`): the Brainstorm works as wanted, grill step 1 is clear.

Bugs (new Issues):
- 004: Brainstorm comes after the merge, not on the Cycle branch (human's call: a Brainstorm may come days later as new work).
- 005: `plugin.json` description must name brainstorm (consistency with the other skills it lists).

For the retro (not this PRD):
- The Kit's own `CHARTER.md` In scope list omits brainstorm; only a retro edits it mid-Cycle (ADR 0006).
- QA should be agent-driven: an agent launches what was built, follows the qa.md steps, explores, and reports findings before the human judges. Today the human had to work out how to load the branch's CLI and plugin (`uv run kit init`, `claude --plugin-dir`). Applies to every Cycle, not just skills: UIs, CLIs, apps.
- Naming a Product after a Brainstorm: the folder is made by `kit init` before the Brainstorm settles what it is, so the name is a guess.
