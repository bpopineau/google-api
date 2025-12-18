---
description: Complete development cycle from analysis to release for mygooglib
---

# /evolve — The Master Development Workflow

This workflow orchestrates the entire mygooglib development lifecycle through 6 phases.

---

## Phase 0: INITIALIZE
**Goal**: Set up tracking to ensure no steps are missed.

### 0.1 Pre-Flight Check
   - `git status --short`
   - **Gate**: Ensure the working directory is clean or you are on a safe feature branch. Do not mix new work with uncommitted changes.

### 0.2 Create Task Artifact
   - Create or update `task.md` with the following structure:
     ```markdown
     # Task: [Feature Name]
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

---

## Phase 1: ANALYZE
**Goal**: Understand project state and identify what to build.

### 1.1 Health Check
// turbo
   - `/health_check`
   - **Gate**: All checks must pass before proceeding.

### 1.2 Coverage Audit
// turbo
   - `/coverage_audit`
   - **Output**: Identifies gaps in API coverage vs AUTOMATION_GOALS.md.

### 1.3 Feature Proposals
// turbo
   - `/propose_features`
   - **Output**: Creates `feature_proposal.md` with prioritized features.

### 1.4 Innovation Ideas (Optional)
   - `/ideate_innovations`
   - **When**: Looking for cross-service workflow ideas.
   - **Output**: Creates `creative_proposals.md`.

---

## Phase 2: PLAN
**Goal**: Get user approval on what to build.

### 2.1 Sanity Check
   - Read `AUTOMATION_GOALS.md` and `docs/development/roadmap.md`.
   - **Gate**: Ensure the proposed work aligns with long-term goals.

### 2.2 Present Analysis
   - Use `notify_user` to present:
     - `coverage_report.md`
     - `feature_proposal.md`
     - (Optional) `creative_proposals.md`

### 2.2 User Approval
   - **Gate**: User must select feature(s) to implement.
   - **Required**: Explicit approval before BUILD phase.

### 2.3 Create Implementation Plan
   - Create `implementation_plan.md` artifact with:
     - Files to modify/create
     - Method signatures
     - Test plan

---

## Phase 3: BUILD
**Goal**: Implement the approved feature.

### 3.1 Scaffold (Optional)
// turbo
   - `/scaffold_new_script`
   - **Create**: Prototype in `scripts/` or `examples/`.
   - **When**: Exploring a new idea before committing to the library.

### 3.2 Implement Core Logic
   - **Location**: `mygooglib/[service].py`
   - **Pattern**: Follow existing methods in the same file.
   - **Imports**: Add to `__all__` if public API.
   - **Important**: Also add methods to the corresponding `[Service]Client` class.

### 3.3 Import Verification
   - `python -c "import mygooglib; print('Imports OK')"`
   - **Gate**: Must print "Imports OK". Catches syntax errors and circular imports early.

### 3.4 Write Unit Tests
   - **Location**: `tests/test_[service].py`
   - **Pattern**: Follow existing test patterns. Add at least one test per new public method.
   - **Run**: `pytest tests/test_[service].py -v`

### 3.4 Cross-Service Integration (If applicable)
// turbo
   - `/cross_service_builder`
   - **When**: Feature combines multiple services.

### 3.5 Add CLI Support (If applicable)
   - **Location**: `mygooglib/cli/[service].py`
   - **Pattern**: Follow existing Typer commands.
   - **Verify**: `mygoog [service] [command] --help`
   - **Import**: Update imports at the top of the CLI file for new library functions.

### 3.6 Lint Check
// turbo
   - `ruff check mygooglib/ tests/`
   - **Gate**: Must pass before proceeding to VERIFY.

---

## Phase 4: VERIFY
**Goal**: Ensure quality before documentation.

### 4.1 Unit Tests
// turbo
   - `pytest tests/ -v`
   - **Gate**: All unit tests must pass.

### 4.2 Smoke Tests
// turbo
   - `python scripts/smoke_test.py all`
   - **Gate**: All services must connect successfully.

### 4.3 Negative Testing
   - **Action**: Intentionally try to break the new feature.
     - Invalid IDs/Paths (e.g., `mygoog drive download "NonExistent"`).
     - Missing arguments.
     - Wrong types.
   - **Gate**: Ensure the app fails gracefully (exit code 1, clear error message), not with a raw traceback.

### 4.4 Manual CLI Verification
   - For each new CLI command:
     1. Run `mygoog [service] [command] --help` to verify registration.
     2. Execute the command with valid test data.
     3. Verify expected output or side effects.
   - **Document**: Note any issues found; loop back to BUILD if needed.

### 4.4 Development Checks (Optional)
// turbo
   - `/development`
   - **Runs**: Format, lint, and full test suite.

### 4.5 Full CI Simulation (Optional)
// turbo
   - `/ci_local`
   - **When**: Before merging to main or releasing.

**Gate**: All tests and verifications must pass. Failures loop back to BUILD.

---

## Phase 5: DOCUMENT
**Goal**: Keep documentation in sync with code.

### 5.1 Docstrings
// turbo
   - `/write_docstrings`
   - **Target**: New methods with Google-style docstrings.
   - **Check**: All public functions have Args, Returns, and Raises sections.

### 5.2 Update Guides
// turbo
   - `/update_docs`
   - **Update**:
     - `docs/guides/usage.md` — add usage examples for new functionality.
     - `README.md` — update if Quick Start or feature list affected.
     - `examples/` — add example script if the feature is complex.

### 5.3 Update Goals
   - **File**: `AUTOMATION_GOALS.md`
   - **Action**: Mark workflow as completed (W1-W6 checkboxes).

### 5.4 Update Roadmap
   - **File**: `docs/development/roadmap.md`
   - **Action**: Check off completed feature, add new ideas if discovered.

### 5.5 Create Walkthrough Artifact
   - **File**: `walkthrough.md` (in artifacts directory).
   - **Contents**:
     - Summary of changes made.
     - Manual verification results.
     - Any new CLI commands with example usage.

---

## Phase 6: RELEASE (Optional)
**Goal**: Ship the feature. Skip this phase for work-in-progress or internal iterations.

### 6.1 Prepare Release
// turbo
   - `/release_prep`
   - **Actions**:
     - Bump version in `pyproject.toml` (if applicable).
     - Update `CHANGELOG.md` with new features and fixes.
     - Stage files: `git add -A`

### 6.2 Final Verification
// turbo
   - `python scripts/smoke_test.py all`
   - **Gate**: Must pass before commit.

### 6.3 Commit and Tag
   - `git commit -m "feat: <description of changes>"`
   - `git tag vX.Y.Z` (if a versioned release).

### 6.4 Push to Origin
   - `git push origin main --tags`
   - **Gate**: Only push if all tests pass and changes are approved.

---

## Quick Reference: Phase Entry Points

| Situation | Start From |
|-----------|------------|
| Fresh feature development | Phase 1 (ANALYZE) |
| User already knows what to build | Phase 3 (BUILD) |
| Hotfix / emergency fix | `/emergency_fix` instead |
| Just updating docs | Phase 5 (DOCUMENT) |
| Ready to ship | Phase 6 (RELEASE) |

---

## Workflow Calls Summary

| Phase | Workflows/Commands Called |
|-------|---------------------------|
| 1. ANALYZE | `/health_check`, `/coverage_audit`, `/propose_features`, `/ideate_innovations` |
| 2. PLAN | *User interaction*, `implementation_plan.md` |
| 3. BUILD | `/scaffold_new_script`, `/cross_service_builder`, `pytest`, `ruff check` |
| 4. VERIFY | `pytest`, `smoke_test.py`, Manual CLI tests, `/development`, `/ci_local` |
| 5. DOCUMENT | `/write_docstrings`, `/update_docs`, `walkthrough.md` |
| 6. RELEASE | `/release_prep`, `smoke_test.py`, `git commit`, `git push` |
