import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_version_matches_pyproject() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    version = project["version"]
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    found = {
        "src/kit/plugin/.claude-plugin/plugin.json": json.loads(
            (ROOT / "src/kit/plugin/.claude-plugin/plugin.json").read_text()
        )["version"],
        ".agents/kit.json": json.loads((ROOT / ".agents/kit.json").read_text())["kit"],
        "src/kit/template/.agents/kit.json": json.loads((ROOT / "src/kit/template/.agents/kit.json").read_text())[
            "kit"
        ],
        "uv.lock": next(p["version"] for p in lock["package"] if p["name"] == project["name"]),
    }
    drift = {path: v for path, v in found.items() if v != version}
    assert not drift, f"pyproject.toml is {version}; these differ: {drift}"
