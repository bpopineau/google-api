---
description: Run mygooglib development workflow (install, lint, test)
---

1. Install mygooglib in editable mode with dev and cli extras
   - `pip install -e ".[dev,cli]"`

2. Format code with ruff
// turbo
   - `ruff format .`

3. Check for linting errors and auto-fix
// turbo
   - `ruff check . --fix`

4. Run unit tests
// turbo
   - `pytest`
   - **Note**: If `tests/` doesn't exist, run `/bootstrap_tests` first.

5. Verify CLI works
// turbo
   - `mygoog --help`

6. Run smoke test (optional, verifies API connectivity)
   - `python scripts/smoke_test.py all`
   - **Reference**: See `docs/development/testing.md` for full smoke test options.
