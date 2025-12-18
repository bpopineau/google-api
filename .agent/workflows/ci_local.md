---
description: Simulate a full CI run locally for mygooglib
---

# /ci_local

**Goal**: Pass all tests before PR/Merge.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve` (Phase 4.5), ensure `task.md` item "CI Simulation" is `[/]`.

---

1. Verify Authentication
// turbo
   - `python scripts/check_token_refresh.py`
   - **Gate**:
     - **IF SUCCESS**: Proceed.
     - **IF FAIL**: Run `/setup_auth` immediately. Stop.

2. Install Latest Dependencies
// turbo
   - `pip install -e ".[dev,cli]"`
   - **Gate**:
     - **IF SUCCESS**: Proceed.
     - **IF FAIL**: Stop. Check network/pypi. Recurse.

3. Format and Lint
// turbo
   - `ruff format .`
   - `ruff check . --fix`
   - **Gate**:
     - **IF CLEAN**: Proceed.
     - **IF ERROR**: Stop. Fix code. Recurse.

4. Run Unit Tests
// turbo
   - `pytest -v`
   - **Gate**:
     - **IF 100% PASS**: Proceed.
     - **IF ANY FAIL**: STOP. Debug and fix. Recurse.

5. Run Smoke Tests (Read-only)
// turbo
   - `python scripts/smoke_test.py all`
   - **Gate**:
     - **IF SUCCESS**: Proceed.
     - **IF FAIL**: STOP. Service issue. Recurse.

6. Verify CLI
// turbo
   - `mygoog --help`
   - **Gate**:
     - **IF WORKS**: Proceed.
     - **IF CRASHES**: Stop. Recurse.

7. (Optional) Generate Coverage
   - `pytest --cov=mygooglib --cov-report=html`
   - `Start-Process "htmlcov/index.html"`

---

**Result**: Mark `[x]` ONLY if step 5 passes with no errors.
