# Python standards

- Type every function signature; pyright strict passes with no ignores.
- ruff check and ruff format pass.
- Tests use pytest, live in `tests/`, and run in seconds without network or Sample data.
- Deep modules: each module exposes a few functions over a substantial inside. Callers never reach past the public names.
- Data transforms are pure functions: data in, data out. Side effects (files, databases, network) sit at the edges.
- Errors are specific exceptions with a message that names the bad value. A bare `except` hides bugs.
- Names come from `CONTEXT.md`.
- Dependencies go through `uv add`; nothing is installed by hand.
