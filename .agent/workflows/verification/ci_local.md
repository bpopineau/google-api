---
description: Simulate a full CI run locally for mygooglib
---

# Workflow: /ci_local

**Role:** DevOps Engineer.

**Context:** Run a complete local CI simulation before PR/Merge.

**Goal:** Pass all tests and quality gates.

---

## Step 1: Verify Authentication

**Task:**
- Execute Atom: `atoms/_auth_check.md`

**Gate:**
- **IF VALID**: Proceed.
- **IF INVALID**: Stop. Run `/maintenance/setup_auth` immediately.

---

## Step 2: Install Dependencies

**Task:**
- Execute Atom: `atoms/_install_deps.md`

**Gate:**
- **IF SUCCESS**: Proceed.
- **IF FAIL**: Stop. Check network/PyPI.

---

## Step 3: Format and Lint

**Task:**
- Execute Atom: `atoms/_lint.md`

**Gate:**
- **IF CLEAN**: Proceed.
- **IF ERROR**: Stop. Fix code.

---

## Step 4: Unit Tests

**Task:**
- Execute Atom: `atoms/_run_tests.md`

**Gate:**
- **IF 100% PASS**: Proceed.
- **IF ANY FAIL**: Stop. Debug and fix.

---

## Step 5: Smoke Tests

**Task:**
- Execute Atom: `atoms/_smoke_test.md`

**Gate:**
- **IF SUCCESS**: Proceed.
- **IF FAIL**: Stop. Service issue.

---

## Step 6: Verify CLI

**Task:**
// turbo
   - `mg --help`

**Gate:**
- **IF WORKS**: Proceed.
- **IF CRASHES**: Stop. Investigate CLI entry point.

---

## Step 7: (Optional) Generate Coverage

**Task:**
   - `pytest --cov=mygooglib --cov-report=html`
   - `Start-Process "htmlcov/index.html"`

---

**Final Output:** JSON
```json
{
  "ci_status": "PASS | FAIL",
  "gates_passed": ["auth", "deps", "lint", "tests", "smoke", "cli"],
  "failed_gate": "<null | gate name>"
}
```

