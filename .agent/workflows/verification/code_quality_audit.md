---
description: Systematically audit for technical debt and sloppiness
---

# /code_quality_audit

**Goal**: Catch the "sloppiness" that linters miss.

## ⚠️ Task Management
- **Rule**: Run this before Phase 4 (VERIFY) or Phase 6 (RELEASE).

---

1. Scan for Debug Leftovers
   - `Select-String -Path "mygooglib\*.py" -Pattern "print\("|"pdb"|"breakpoint"|"# DEBUG" -Recurse`
   - **Gate**:
     - **IF FOUND**: STOP. Remove all debug artifacts. Recurse.
     - **IF CLEAN**: Proceed.

2. Scan for Technical Debt
   - `Select-String -Path "mygooglib\*.py" -Pattern "TODO"|"FIXME"|"HACK" -Recurse`
   - **Gate**:
     - **IF NEW ITEMS**: STOP. Are these required now?
       - YES: Fix them.
       - NO: Move to `docs/development/roadmap.md` or `AUTOMATION_GOALS.md`.
     - **IF CLEAN**: Proceed.

3. Verify Type Safety (The Strict Check)
   - Scan for explicit `Any` without justification.
   - `Select-String -Path "mygooglib\*.py" -Pattern ": Any"|"-> Any" -Recurse`
   - **Gate**:
     - **IF JUSTIFIED** (e.g., JSON payload): Proceed.
     - **IF LAZY** (e.g., `def foo(x: Any)`): STOP. Define explicit type or Protocol. Recurse.

4. Check "The Big Three" (Docs, Tests, exports)
   - **Exports**: Is the new function added to `__init__.py`?
   - **Docs**: Does `help(method)` look professional?
   - **Tests**: unique test file exists?
   - **Gate**:
     - **IF YES**: Proceed.
     - **IF NO**: STOP. Fix the missing artifact. Recurse.

5. Complexity Check (The Eyeball Test)
   - Scan for functions > 50 lines or > 5 arguments.
   - **Gate**:
     - **IF COMPLEX**: STOP. Can it be split?
       - YES: Refactor.
       - NO: Add extensive comments explaining why.

---

**Result**: Mark `[x]` for "Quality Audit" in `task.md`.
