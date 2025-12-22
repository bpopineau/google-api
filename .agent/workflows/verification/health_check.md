---
description: Quick project health verification before any work
---

# /health_check

**Goal**: Verify the environment is ready for work.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve`, ensure `task.md` item "Health Check" is marked `[/]` BEFORE starting.

---

1. Verify Git State
// turbo
   - `git status --short`
   - **Gate**:
     - **IF CLEAN**: Proceed.
     - **IF DIRTY**: Stop. Commit or stash changes. Recurse.

2. Verify Dependencies
// turbo
   - `pip install -e ".[dev,cli]"`
   - **Gate**:
     - **IF SUCCESS**: Proceed.
     - **IF FAIL**: Stop. Fix pip/network issues. Recurse.

3. Verify Core Import
// turbo
   - `python -c "from mygooglib import get_clients; print('Import OK')"`
   - **Gate**:
     - **IF "Import OK"**: Proceed.
     - **IF ERROR**: Stop. Fix syntax/environment. Recurse.

4. Verify Authentication
// turbo
   - `python scripts/check_token_refresh.py`
   - **Gate**:
     - **IF SUCCESS**: Proceed.
     - **IF FAIL**: Run `/setup_auth`. Recurse.

5. Quick Smoke Test
// turbo
   - `python scripts/smoke_test.py all`
   - **Gate**:
     - **IF PASS**: Proceed.
     - **IF FAIL**: Stop. Debug specific service error. Recurse.

6. Verify CLI
// turbo
   - `mg --help`
   - **Gate**:
     - **IF SHOWS HELP**: proceeding.
     - **IF ERROR**: Stop. Fix entry point. Recurse.

---

**Result**: If all gates passed, mark "Health Check" as `[x]` in `task.md`.

