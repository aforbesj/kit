import ast
import subprocess
from pathlib import Path


def test_ruff_format_is_clean() -> None:
    result = subprocess.run(
        ["uv", "run", "ruff", "format", "--check", "src", "tests"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_signature_is_typed() -> None:
    root = Path(__file__).resolve().parent.parent
    missing: list[str] = []
    for folder in ("src", "tests"):
        for path in sorted((root / folder).rglob("*.py")):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                args = node.args
                params = [*args.posonlyargs, *args.args, *args.kwonlyargs]
                if args.vararg:
                    params.append(args.vararg)
                if args.kwarg:
                    params.append(args.kwarg)
                untyped = [a.arg for a in params if a.annotation is None and a.arg not in ("self", "cls")]
                if node.returns is None or untyped:
                    rel = path.relative_to(root)
                    missing.append(f"{rel}:{node.lineno} {node.name}")
    assert not missing, "untyped signatures: " + ", ".join(missing)
