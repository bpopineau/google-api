---
description: Systematically identify, reproduce, and fix mygooglib issues
---

# Workflow: /debug_issue

## Phase 1: Context Analysis

**Role:** Systems Architect.

**Task:**
- Execute Atom: `atoms/_analyze_files.md`
- Understand the current state and recent changes.

---

## Phase 2: Reproduction

**Role:** Senior Site Reliability Engineer (SRE).

**Context:** Isolate and reproduce the issue before attempting a fix.

**Task:**
1. Create `scripts/repro.py` with minimal reproduction code:
   ```python
   from mygooglib import get_clients
   clients = get_clients()
   # Reproduce the failing operation here
   ```
2. Alternative: Create a test in `tests/test_[module].py` to capture the failure.

**Constraints:**
- Do NOT attempt a fix until the issue is reproducible.

---

## Phase 3: Root Cause Analysis

**Role:** Principal Debugging Engineer.

**Context:** Locate the source of the bug.

**Task:**
1. Read traceback and identify the failing module in `mygooglib/`.
2. Search codebase: `Select-String -Path "mygooglib\*.py" -Pattern "error_message" -Recurse`
3. Check utilities: `mygooglib/utils/` for retry/logging issues.
4. Use debugger if needed: `python -m pdb scripts/repro.py`

**Output:** Identify the exact file, function, and line causing the issue.

---

## Phase 4: Implementation

**Role:** Senior Software Engineer.

**Task:**
1. Implement the smallest possible fix.
2. Follow existing patterns in the file.

**Constraints:**
- Minimal viable fix only. Do not refactor unrelated code.

---

## Phase 5: Verification

**Role:** QA Automation Engineer.

**Task:**
1. Run repro script: `python scripts/repro.py` (should succeed).
2. Or run specific test: `pytest tests/test_[module].py::test_specific_case -v`

---

## Phase 6: Regression Check

**Role:** QA Automation Engineer.

**Task:**
- Execute Atom: `atoms/_lint.md`
- Execute Atom: `atoms/_run_tests.md`
- Execute Atom: `atoms/_smoke_test.md`

---

## Phase 7: Cleanup

**Role:** Release Engineer.

**Task:**
1. Delete `scripts/repro.py` or promote to `tests/test_[module].py`.
2. Remove debug prints.

**Finalize:**
- Execute Atom: `atoms/_checkpoint.md` (message: "fix: resolved issue in [module]")
