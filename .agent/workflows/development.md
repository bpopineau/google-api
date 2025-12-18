---
description: Standard development workflow for setup, linting, and testing
---

1. Install project in editable mode with dev and cli dependencies
   - `pip install -e ".[dev,cli]"`

2. Format code
// turbo
   - `ruff format .`

3. Check for linting errors
// turbo
   - `ruff check . --fix`

4. Run unit tests
// turbo
   - `pytest`

5. Run smoke test (optional, verifies basic connectivity)
   - `python scripts/smoke_test.py`
