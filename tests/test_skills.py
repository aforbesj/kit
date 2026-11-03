from pathlib import Path

SKILLS = Path(__file__).parent.parent / "src/kit/plugin/skills"


def _brainstorm() -> str:
    return (SKILLS / "brainstorm/SKILL.md").read_text()


def _body(text: str) -> list[str]:
    return text.split("---\n", 2)[2].strip().splitlines()


def test_brainstorm_skill_is_manual_only() -> None:
    text = _brainstorm()
    assert "name: brainstorm\n" in text
    assert "disable-model-invocation: true\n" in text


def test_brainstorm_ends_at_grill_and_writes_no_file() -> None:
    body = _body(_brainstorm())
    assert "/kit:grill" in body[-1]
    assert not any(
        "write" in line.lower() and "file" in line.lower() and "no file" not in line.lower() for line in body
    )


def test_brainstorm_body_is_short() -> None:
    assert len(_body(_brainstorm())) <= 25


def test_grill_points_empty_charter_to_brainstorm_and_widens_after_one() -> None:
    text = (SKILLS / "grill/SKILL.md").read_text()
    assert "/kit:brainstorm" in text
    assert "Charter grill" in text
    assert "after a Brainstorm" in text
    assert "add Features" in text and "widen scope" in text


def test_template_charter_names_charter_grill_and_retro() -> None:
    text = (SKILLS.parent.parent / "template/CHARTER.md").read_text()
    assert "only a retro edits it" not in text
    assert "Charter grill" in text and "retro" in text


def test_retro_points_empty_area_to_brainstorm() -> None:
    text = (SKILLS / "retro/SKILL.md").read_text()
    assert "/kit:brainstorm" in text
    assert "Remove the finished Feature from `CHARTER.md` and name the next one" in text


ROOT = Path(__file__).parent.parent


def test_claude_md_copies_match_and_name_brainstorm() -> None:
    a = (ROOT / "CLAUDE.md").read_text()
    assert a == (ROOT / "src/kit/template/CLAUDE.md").read_text()
    phases = next(line for line in a.splitlines() if line.startswith("Phases:"))
    assert "Brainstorm" in phases


def test_readme_names_brainstorm_in_start_and_close() -> None:
    text = (ROOT / "README.md").read_text()
    start = text.split("## Start a Product")[1].split("## Run a Cycle")[0]
    close = next(line for line in text.splitlines() if line.startswith("| Close"))
    assert "/kit:brainstorm" in start
    assert "/kit:brainstorm" in close


def test_retro_runs_brainstorm_after_close_and_merge() -> None:
    text = (SKILLS / "retro/SKILL.md").read_text()
    assert text.index("kit close <area>") < text.index("/kit:brainstorm")
    assert "after the merge" in text


def test_readme_close_row_brainstorms_after_merge() -> None:
    text = (ROOT / "README.md").read_text()
    close = next(line for line in text.splitlines() if line.startswith("| Close"))
    assert close.index("After the merge") < close.index("/kit:brainstorm")
    assert close.index("/kit:grill") < close.index("/kit:brainstorm")


def test_plugin_description_names_brainstorm_before_grill() -> None:
    import json

    manifest = json.loads((SKILLS.parent / ".claude-plugin/plugin.json").read_text())
    desc = manifest["description"]
    assert desc.index("brainstorm") < desc.index("grill")


def test_marketplace_description_matches_plugin_manifest() -> None:
    import json

    manifest = json.loads((SKILLS.parent / ".claude-plugin/plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    entry = next(p for p in market["plugins"] if p["name"] == "kit")
    assert entry["description"] == manifest["description"]
