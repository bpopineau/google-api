---
description: "This workflow enforces a simple 3-phase cycle: **PLAN**, **BUILD**, **SHIP**. `task.md` is the source of truth for all progress."
---

# Workflow: /evolve

## Phase 0: PRE-FLIGHT

**Role:** Build Engineer.

**Task:**
1. Ensure virtual environment is activated (`.venv`).
2. Run `where python` (Windows) to verify.

---

## Phase 1: PLAN

**Role:** Principal Architect.

**Context:** Gather context before any action.

**Task:**
1. Execute Atom: `atoms/_analyze_files.md`
2. **Identify Goal:** Ask user: "Do you have a specific goal, or should I propose features?"
   - *No Goal?* Suggest `@[/planning/ideate_innovations]` or `@[/planning/propose_features]`.
   - *Have Goal?* Suggest `@[/planning/plan_feature]`.
3. **Codebase Review:** *MANDATORY*. Review relevant files before committing to a plan.
4. **Initialize `task.md`:** Create task file with PLAN/BUILD/SHIP structure.
5. **Break down work:** Add specific implementation steps under BUILD.

**Constraints:**
- Do NOT proceed to BUILD until user explicitly approves the plan.

**Output:** Summary of plan (Goal, Changes, Verification steps).

---

## Phase 2: BUILD

**Role:** Senior Software Engineer.

**Context:** Execute the approved plan.

**Task:**
1. Work through the checklist in `task.md`.
2. Write unit tests for new functionality immediately.
3. Quality Check:
   - Execute Atom: `atoms/_run_tests.md`
   - Execute Atom: `atoms/_lint.md`
4. Mark items `[x]` in `task.md` ONLY after verified.

**Constraints:**
- Test frequently.
- Verify each task individually before marking complete.

---

## Phase 3: SHIP

**Role:** Release Manager.

**Context:** Mandatory gate before merge.

### Step 1: Smoke Tests
**Task:**
- Execute Atom: `atoms/_smoke_test.md`

### Step 2: Documentation (Mandatory)
**Task:**
1. Ensure new code has Google-style docstrings.
2. Consider `@[/maintenance/update_docs]` if significant changes.
3. Update README with new features.

### Step 3: Changelog
**Task:**
- Add concise entry to `CHANGELOG.md`.

### Step 4: Release (Optional)
**Task:**
- Consider `@[/lifecycle/release_prep]` if named release.
- Bump version in `pyproject.toml`.

### Step 5: Commit & Push
**Task:**
1. Run `git status` to review changes.
2. Execute Atom: `atoms/_checkpoint.md`
3. Run `git push`.

---

**Final Output:** JSON
```json
{
  "workflow_status": "COMPLETE | BLOCKED",
  "phase_completed": "PLAN | BUILD | SHIP",
  "blockers": ["<list of issues>"]
}
```