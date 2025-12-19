---
description: Systematically refactor mygooglib code with safety checks
---

# Workflow: /refactor

## Phase 1: Context Analysis

**Role:** Systems Architect.

**Context:** Before any refactoring, we must understand the codebase.

**Task:**
- Execute Atom: `atoms/_analyze_files.md`
- **Constraint:** Use the "Thinking First" rule. Break down the current implementation's complexity before suggesting changes.

---

## Phase 2: Architectural Review

**Role:** Principal Architect.

**Context:** Review the target code for architectural issues.

**Task:**
1. Identify the target for refactoring (function/class/module in `mygooglib/`).
2. Review for adherence to SOLID principles.
3. Identify code smells:
   - Duplicated patterns across services
   - Long methods (extract to `mygooglib/utils/`)
   - Magic strings/numbers (extract to constants)

**Constraints:**
- Do NOT write code yet.
- If modifying public API (functions in `__all__`), plan deprecation warnings.

**Output:** Generate a step-by-step refactoring plan. Request user approval before proceeding.

---

## Phase 3: Safety Checkpoint

**Role:** Release Engineer.

**Task:**
- Execute Atom: `atoms/_checkpoint.md` (message: "checkpoint: before refactor")

---

## Phase 4: Execution

**Role:** Senior Software Engineer.

**Context:** Apply the approved refactoring plan.

**Task:**
1. Execute the plan from Phase 2.
2. Make changes incrementally (one method/class at a time).
3. Run `pytest` after each logical chunk.

**Constraints:**
- Maintain existing function signatures to prevent breaking changes unless explicitly authorized.
- Follow existing code patterns in the file.

---

## Phase 5: Verification

**Role:** QA Automation Engineer.

**Task:**
- Execute Atom: `atoms/_lint.md`
- Execute Atom: `atoms/_run_tests.md`
- Execute Atom: `atoms/_smoke_test.md`

**Constraints:**
- If tests fail, rollback changes and output error log using "Root Cause Analysis" framework.
- Refactoring should NOT change behavior.

---

## Phase 6: Documentation & Cleanup

**Role:** Technical Writer.

**Task:**
1. If signature changed, update `docs/guides/usage.md`.
2. If internal architecture changed, update `docs/reference/design_principles.md`.
3. Run `/development/write_docstrings` if docstrings need updating.
4. Remove unused imports (`ruff check . --select F401`).

**Finalize:**
- Execute Atom: `atoms/_checkpoint.md` (message: "refactor: applied improvements to [module]")
