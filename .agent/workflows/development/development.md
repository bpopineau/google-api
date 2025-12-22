---
description: Run mygooglib development workflow (install, lint, test)
---

# /development

**Goal**: Verify code correctness before push.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve` (Phase 4), ensure `task.md` item "Development Checks" is `[/]`.

---

1. Install
   - `pip install -e ".[dev,cli]"`
   - **Gate**:
     - **IF SUCCESS**: Proceed.
     - **IF FAIL**: Stop. Fix env. Recurse.

2. Format & Lint
// turbo
   - `ruff format .`
   - `ruff check . --fix`
   - **Gate**:
     - **IF CLEAN**: Proceed.
     - **IF ERRORS**: Stop. Fix issues manually if listed. Recurse.

3. Run Unit Tests
// turbo
   - `pytest`
   - **Gate**:
     - **IF ALL PASS**: Proceed.
     - **IF FAILURES**: Stop. Fix code. Recurse.

4. Verify CLI
// turbo
   - `mg --help`
   - **Gate**:
     - **IF WORKS**: Proceed.
     - **IF CRASHES**: Stop. Fix entrypoint. Recurse.

5. Run Smoke Test (Read-only)
   - `python scripts/smoke_test.py all`
   - **Gate**:
     - **IF CONNECTS**: Proceed.
     - **IF FAILS**: Stop. Debug. Recurse.

---

**Result**: Mark `[x]` for the check in `task.md`.

