---
description: "This workflow enforces a simple 3-phase cycle: **PLAN**, **BUILD**, **SHIP**. `task.md` is the source of truth for all progress."
---

# Workflow: /evolve

## Phase 0: PRE-FLIGHT

**Role:** DevOps Engineer

**Goal:** Ensure a deterministic build environment.

**Task:**
1. **Environment Check:**
   - Verify `uv` is installed: `uv --version`
   - Sync dependencies to lockfile: `uv sync`
   - Verify shell: `Get-Command python` (PowerShell) or `which python` (Bash) to confirm paths.

2. **Clean State:**
   - Ensure git is clean: `git status --short`. (Stash or commit if dirty).

---

## Phase 1: PLAN

**Role:** Principal Architect

**Goal:** Define *what* to build before writing code.

**Protocol:**
1. **Context Analysis:**
   - Review `AUTOMATION_GOALS.md` and `docs/development/roadmap.md`.
   - *Action:* If ambiguous, ask user for clarification.
2. **Task Artifact Creation:**
   - Create or overwrite `task.md` with the implementation plan.
   - **Critical Rule:** The `task.md` is the Single Source of Truth.
   - **Template:**
     ```markdown
     # [Feature Name]
     
     ## Phase 1: Planning
     - [x] Context Analysis
     
     ## Phase 2: Implementation
     - [ ] Core Logic: [Component A]
     - [ ] Core Logic: [Component B]
     - [ ] Tests: Unit tests for A & B
     - [ ] CLI: Command structure
     
     ## Phase 3: Verification
     - [ ] Lint (`ruff check`)
     - [ ] Tests (`pytest`)
     - [ ] Smoke Test (`scripts/smoke_test.py`)
     ```

**Output:** Present the Plan to the user. **STOP** and wait for approval.

---

## Phase 2: BUILD

**Role:** Senior Software Engineer

**Goal:** Execute the plan with Test-Driven Development (TDD).

**Loop Protocol:**
For each unchecked item in `task.md`:
1. **Mark In-Progress:** Change `[ ]` to `[/]`.
2. **Implement:** Write the code or test.
   - *Constraint:* Write unit tests in `tests/` *concurrently* with code in `mygooglib/`.
3. **Micro-Verify:**
   - Lint: `uv run ruff check . --fix`
   - Test: `uv run pytest tests/test_specific_feature.py`
4. **Mark Complete:** Change `[/]` to `[x]` ONLY after the micro-verification passes.

---

## Phase 3: SHIP

**Role:** Release Manager

**Goal:** Quality Assurance and release packaging.

**Task:**
1. **Full Suite Verification:**
   - Run entire test suite: `uv run pytest`
   - Run Type/Lint check: `uv run ruff check .` and `uv run ruff format .`
   - **Smoke Test:** Execute `uv run python scripts/smoke_test.py all`.
     - *Gate:* If this fails, DO NOT SHIP. Fix and recurse to Phase 2.

2. **Documentation Update:**
   - Update `README.md` features list.
   - Ensure `docs/guides/usage.md` reflects new CLI commands.

3. **Release Artifacts:**
   - Bump version in `pyproject.toml` (if applicable).
   - Update `CHANGELOG.md` with a concise entry.

4. **Final Output:**
   - Provide a summary JSON:
   ```json
   {
     "status": "READY_TO_MERGE",
     "files_changed": ["list", "of", "files"],
     "tests_passed": true
   }
