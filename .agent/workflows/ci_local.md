---
description: Simulate a full CI run locally for mygooglib
---

1. Verify Authentication
// turbo
   - `python scripts/check_token_refresh.py`
   - **Fail fast**: If token refresh fails, run `/setup_auth`.

2. Install Latest Dependencies
// turbo
   - `pip install -e ".[dev,cli]"`

3. Format and Lint
// turbo
   - `ruff format .`
   - `ruff check . --fix`

4. Run Unit Tests
// turbo
   - `pytest -v`

5. Run Smoke Tests (read-only)
// turbo
   - `python scripts/smoke_test.py all`
   - **Tests**: Drive, Sheets, Gmail, Calendar, Tasks connectivity.

6. Verify CLI
// turbo
   - `mygoog --help`
   - `mygoog drive list --help`
   - `mygoog sheets read --help`

7. (Optional) Generate Coverage Report
   - `pytest --cov=mygooglib --cov-report=html`
   - **View**: Open `htmlcov/index.html` in browser.

8. (Optional) Run Write Tests
   - `python scripts/smoke_test.py all --write`
   - **Warning**: This mutates real data (sends email, writes to Sheets).
