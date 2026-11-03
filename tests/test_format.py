import subprocess


def test_ruff_format_is_clean():
    result = subprocess.run(
        ["uv", "run", "ruff", "format", "--check", "src", "tests"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
