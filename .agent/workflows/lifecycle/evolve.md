---
description: "This workflow enforces a simple 3-phase cycle: **PLAN**, **BUILD**, **SHIP**. `task.md` is the source of truth for all progress."
---

// turbo-all
# Workflow: /evolve

## Phase 0: PRE-FLIGHT

**Role:** Build Engineer.

**Task:**
1. Ensure virtual environment is activated (`.venv`).
2. Run `uv --version` to verify `uv` is installed.
3. Run `where python` (Windows) to verify paths.

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
4. **Initialize `task.md`:** Create task file with the following structure:
   ```markdown
   # [Feature Name]
   
   - [ ] Phase 1: Planning & Research <!-- id: 0 -->
   - [ ] Phase 2: Implementation <!-- id: 1 -->
   - [ ] Phase 3: Verification <!-- id: 2 -->
   ```
5. **Break down work:** Add specific implementation steps under BUILD.

**Constraints:**
- Do NOT proceed to BUILD until user explicitly approves the plan via `implementation_plan.md`.

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
- Execute Atom: `atoms/_update_docs.md` or `atoms/_write_docstrings.md`.
- Update README with new features if applicable.

### Step 3: Changelog
**Task:**
- Add concise entry to `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

### Step 4: Release & Checkpoint
**Task:**
- Bump version in `pyproject.toml` if this is a named release.
- Execute Atom: `atoms/_checkpoint.md`

---

**Final Output:** JSON
```json
{
  "workflow_status": "COMPLETE | BLOCKED",
  "phase_completed": "PLAN | BUILD | SHIP",
  "blockers": ["<list of issues>"]
}
```