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
