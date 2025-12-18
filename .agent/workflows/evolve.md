---
description: Complete development cycle from analysis to release for mygooglib
---

# /evolve — The Master Development Workflow

This workflow orchestrates the entire mygooglib development lifecycle through 6 phases.

---

## ⚠️ CRITICAL: Task List Management Rules

**These rules are NON-NEGOTIABLE. Follow them exactly.**

### Rule 1: Task.md is the Single Source of Truth
- The `task.md` artifact tracks ALL work items
- NEVER skip ahead without updating `task.md` first
- ALWAYS verify `task.md` reflects current state before proceeding

### Rule 2: State Markers
Use these exact markers in `task.md`:
- `[ ]` = Not started
- `[/]` = In progress
- `[x]` = Complete

### Rule 3: The BEFORE/DURING/AFTER Protocol
For EVERY sub-task:

1. **BEFORE starting a task**:
   - Read `task.md` to verify current state
   - Mark the task as `[/]` (in progress)
   
2. **DURING the task**:
   - Do the actual work
   - If work spawns sub-items, add them to `task.md`
   
3. **AFTER completing a task**:
   - Verify the work is actually done
   - Mark the task as `[x]` (complete)
   - Read `task.md` to identify the NEXT uncompleted task

### Rule 4: Gate Verification
At each **Gate** checkpoint:
1. Read `task.md` 
2. Verify ALL prior items in the phase are `[x]`
3. If any are `[ ]` or `[/]`, complete them FIRST
4. Only proceed when gate conditions are met

### Rule 5: Phase Transitions
When moving from Phase N to Phase N+1:
1. Verify ALL items in Phase N are `[x]`
2. Mark Phase N itself as `[x]`
3. Read `implementation_plan.md` (if in BUILD/VERIFY) to cross-check ALL planned work

---

## Phase 0: INITIALIZE

**Goal**: Set up tracking to ensure no steps are missed.

### 0.1 Pre-Flight Check
// turbo
```powershell
git status --short
```
- **Gate**: Working directory is clean OR you are on a safe feature branch.

### 0.2 Create Task Artifact
- **BEFORE**: Confirm no existing `task.md` conflicts
- **ACTION**: Create `task.md` with this EXACT structure:

```markdown
# Task: Evolve Development Cycle

- [ ] Phase 0: INITIALIZE
    - [ ] Pre-Flight Check (`git status`)
    - [ ] Create Task Artifact
- [ ] Phase 1: ANALYZE
    - [ ] Health Check (`/health_check`)
    - [ ] Coverage Audit (`/coverage_audit`)
    - [ ] Feature Proposals (`/propose_features`)
- [ ] Phase 2: PLAN
    - [ ] Check Goals (`AUTOMATION_GOALS.md`)
    - [ ] Present Analysis
    - [ ] Create Implementation Plan
- [ ] Phase 3: BUILD
    - [ ] Scaffold (Optional)
    - [ ] Implement Core Logic
    - [ ] Import Verification
    - [ ] Write Unit Tests
    - [ ] CLI Support (Optional)
    - [ ] Lint Check
- [ ] Phase 4: VERIFY
    - [ ] Unit Tests (`pytest`)
    - [ ] Smoke Tests (`smoke_test.py`)
    - [ ] Negative Testing (Failure modes)
    - [ ] Manual Check
- [ ] Phase 5: DOCUMENT
    - [ ] Docstrings
    - [ ] Guides/README
    - [ ] Walkthrough Artifact
- [ ] Phase 6: RELEASE (Optional)
    - [ ] Release Prep
    - [ ] Final Verification
    - [ ] Push
```

- **AFTER**: Mark "Create Task Artifact" as `[x]`, mark Phase 0 as `[x]`

---

## Phase 1: ANALYZE

**Goal**: Understand project state and identify what to build.

### 1.1 Health Check
- **BEFORE**: Mark `Health Check` as `[/]` in `task.md`
// turbo
- Run `/health_check` workflow
- **Gate**: All checks must pass
- **AFTER**: Mark `Health Check` as `[x]`

### 1.2 Coverage Audit
- **BEFORE**: Mark `Coverage Audit` as `[/]` in `task.md`
// turbo
- Run `/coverage_audit` workflow
- **Output**: `coverage_report.md` artifact
- **AFTER**: Mark `Coverage Audit` as `[x]`

### 1.3 Feature Proposals  
- **BEFORE**: Mark `Feature Proposals` as `[/]` in `task.md`
// turbo
- Run `/propose_features` workflow
- **Output**: `feature_proposal.md` artifact
- **AFTER**: Mark `Feature Proposals` as `[x]`, mark Phase 1 as `[x]`

---

## Phase 2: PLAN

**Goal**: Get user approval on what to build.

### 2.1 Check Goals
- **BEFORE**: Mark `Check Goals` as `[/]` in `task.md`
- Read `AUTOMATION_GOALS.md` and `docs/development/roadmap.md`
- **Gate**: Proposed work must align with documented goals
- **AFTER**: Mark `Check Goals` as `[x]`

### 2.2 Present Analysis
- **BEFORE**: Mark `Present Analysis` as `[/]` in `task.md`
- Use `notify_user` to present findings and get approval
- **Gate**: User must explicitly approve feature(s) to implement
- **AFTER**: Mark `Present Analysis` as `[x]`

### 2.3 Create Implementation Plan
- **BEFORE**: Mark `Create Implementation Plan` as `[/]` in `task.md`
- Create `implementation_plan.md` with:
  - **ALL files to modify/create** (numbered list)
  - **ALL method signatures** 
  - **ALL CLI commands**
  - **ALL test files and test cases**
- **AFTER**: Mark `Create Implementation Plan` as `[x]`, mark Phase 2 as `[x]`

---

## Phase 3: BUILD

**Goal**: Implement the approved feature.

### ⚠️ BUILD Phase Specific Rules

**Before starting BUILD:**
1. Read `implementation_plan.md` completely
2. Extract EVERY deliverable into `task.md` as sub-items under "Implement Core Logic"
3. Example: If plan says "add 3 functions + 2 CLI commands", add:
   ```markdown
   - [ ] Implement Core Logic
       - [ ] Function: create_contact
       - [ ] Function: update_contact
       - [ ] Function: delete_contact
       - [ ] Client method: ContactsClient.create_contact
       - [ ] Client method: ContactsClient.update_contact
       - [ ] Client method: ContactsClient.delete_contact
       - [ ] CLI: mygoog contacts add
       - [ ] CLI: mygoog contacts update
       - [ ] CLI: mygoog contacts delete
   ```

### 3.1 Scaffold (Optional)
- **WHEN**: Exploring a new idea
- Run `/scaffold_new_script` if needed

### 3.2 Implement Core Logic
- **BEFORE**: Mark each sub-item as `[/]` BEFORE implementing it
- **Location**: `mygooglib/[service].py`
- **Pattern**: Follow existing methods
- **Exports**: Add to `__all__` if public
- **Client Methods**: MUST also add to `[Service]Client` class
- **AFTER**: Mark each sub-item as `[x]` AFTER completing it

### 3.3 Import Verification
- **BEFORE**: Mark `Import Verification` as `[/]`
// turbo
```powershell
.\.venv\Scripts\Activate.ps1; python -c "from mygooglib import get_clients; print('Import OK')"
```
- **Gate**: Must print "Import OK"
- **AFTER**: Mark `Import Verification` as `[x]`

### 3.4 Write Unit Tests
- **BEFORE**: Cross-check `implementation_plan.md` for ALL planned test cases
- Add tests matching plan to `task.md`:
   ```markdown
   - [ ] Write Unit Tests
       - [ ] test_create_contact_builds_correct_request
       - [ ] test_update_contact_with_etag
       - [ ] test_delete_contact_calls_api
   ```
- **Location**: `tests/test_[feature].py`
- **AFTER**: Mark each test as `[x]` after writing

### 3.5 CLI Support (If applicable)
- **BEFORE**: Cross-check `implementation_plan.md` for ALL planned CLI commands
- **Location**: `mygooglib/cli/[service].py`
- **Verify**: `mygoog [service] [command] --help` must work
- **AFTER**: Mark `CLI Support` as `[x]`

### 3.6 Lint Check
- **BEFORE**: Mark `Lint Check` as `[/]`
// turbo
```powershell
.\.venv\Scripts\Activate.ps1; ruff check mygooglib/ tests/
```
- **Gate**: Must pass
- **AFTER**: Mark `Lint Check` as `[x]`, mark Phase 3 as `[x]`

### BUILD Phase Exit Gate
**BEFORE leaving BUILD phase:**
1. Read `implementation_plan.md` 
2. For EACH item in "Proposed Changes", verify it was implemented
3. For EACH item in "Verification Plan", verify tests exist
4. If ANYTHING is missing, implement it before proceeding

---

## Phase 4: VERIFY

**Goal**: Ensure quality before documentation.

### 4.1 Unit Tests
- **BEFORE**: Mark `Unit Tests` as `[/]`
// turbo
```powershell
.\.venv\Scripts\Activate.ps1; pytest tests/ -v
```
- **Gate**: ALL tests must pass
- **AFTER**: Mark `Unit Tests` as `[x]`

### 4.2 Smoke Tests
- **BEFORE**: Mark `Smoke Tests` as `[/]`
// turbo
```powershell
.\.venv\Scripts\Activate.ps1; python scripts/smoke_test.py all
```
- **Gate**: All services must connect
- **AFTER**: Mark `Smoke Tests` as `[x]`

### 4.3 Negative Testing
- **BEFORE**: Mark `Negative Testing` as `[/]`
- Test failure modes: invalid IDs, missing args, wrong types
- **Gate**: Errors are graceful, not raw tracebacks
- **AFTER**: Mark `Negative Testing` as `[x]`

### 4.4 Manual Check
- **BEFORE**: Mark `Manual Check` as `[/]`
- For each new CLI command, run `--help` and verify with real data
- **AFTER**: Mark `Manual Check` as `[x]`, mark Phase 4 as `[x]`

---

## Phase 5: DOCUMENT

**Goal**: Keep documentation in sync with code.

### 5.1 Docstrings
- **BEFORE**: Mark `Docstrings` as `[/]`
- Ensure all new public functions have Google-style docstrings
- **AFTER**: Mark `Docstrings` as `[x]`

### 5.2 Update Guides
- **BEFORE**: Mark `Guides/README` as `[/]`
- Update `docs/guides/usage.md` if needed
- Update `README.md` if feature list affected
- **AFTER**: Mark `Guides/README` as `[x]`

### 5.3 Create Walkthrough Artifact
- **BEFORE**: Mark `Walkthrough Artifact` as `[/]`
- Create `walkthrough.md` with:
  - Summary of changes
  - Test results
  - New CLI commands with examples
- **AFTER**: Mark `Walkthrough Artifact` as `[x]`, mark Phase 5 as `[x]`

---

## Phase 6: RELEASE (Optional)

**Goal**: Ship the feature.

### 6.1 Release Prep
- **BEFORE**: Mark `Release Prep` as `[/]`
- Bump version in `pyproject.toml`
- Update `CHANGELOG.md`
- Stage files: `git add .`
- **AFTER**: Mark `Release Prep` as `[x]`

### 6.2 Final Verification
- **BEFORE**: Mark `Final Verification` as `[/]`
// turbo
```powershell
.\.venv\Scripts\Activate.ps1; python scripts/smoke_test.py all
```
- **Gate**: Must pass before commit
- **AFTER**: Mark `Final Verification` as `[x]`

### 6.3 Push
- **BEFORE**: Mark `Push` as `[/]`
- Commit: `git commit -m "feat: <description>"`
- Push: `git push`
- **AFTER**: Mark `Push` as `[x]`, mark Phase 6 as `[x]`

---

## Quick Reference

| Situation | Start From |
|-----------|------------|
| Fresh feature development | Phase 1 (ANALYZE) |
| User already knows what to build | Phase 3 (BUILD) |
| Hotfix / emergency fix | `/emergency_fix` instead |
| Just updating docs | Phase 5 (DOCUMENT) |
| Ready to ship | Phase 6 (RELEASE) |

---

## Checklist Verification Commands

Use these to verify task.md state at any point:

```powershell
# Count incomplete items
Select-String -Path "task.md" -Pattern "\[ \]" | Measure-Object

# Count in-progress items  
Select-String -Path "task.md" -Pattern "\[/\]" | Measure-Object

# Count complete items
Select-String -Path "task.md" -Pattern "\[x\]" | Measure-Object
```

