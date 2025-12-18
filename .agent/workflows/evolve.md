---
description: Complete development cycle from analysis to release for mygooglib
---

# /evolve — The Master Development Workflow

This workflow orchestrates the entire mygooglib development lifecycle through 6 phases.

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

### 2.1 Present Analysis
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

### 3.1 Scaffold
// turbo
   - `/scaffold_new_script`
   - **Create**: Prototype in `scripts/` or `examples/`.

### 3.2 Implement Core Logic
   - **Location**: `mygooglib/[service].py`
   - **Pattern**: Follow existing methods in the same file.
   - **Imports**: Add to `__all__` if public API.

### 3.3 Cross-Service Integration (If applicable)
// turbo
   - `/cross_service_builder`
   - **When**: Feature combines multiple services.

### 3.4 Add CLI Support (If applicable)
   - **Location**: `mygooglib/cli/[service].py`
   - **Pattern**: Follow existing Typer commands.
   - **Test**: `mygoog [service] [command] --help`

---

## Phase 4: VERIFY
**Goal**: Ensure quality before documentation.

### 4.1 Development Checks
// turbo
   - `/development`
   - **Runs**: Format, lint, unit tests.

### 4.2 Full CI Simulation
// turbo
   - `/ci_local`
   - **Runs**: Auth check, tests, smoke tests, CLI verification.

### 4.3 API Verification
// turbo
   - `/verify_installation`
   - **Runs**: Smoke tests against real Google APIs.

### 4.4 Add Missing Tests
   - If new functionality lacks tests:
// turbo
   - `/bootstrap_tests`
   - **Add**: `tests/test_[service].py::test_[new_method]`

**Gate**: All tests must pass. Failures loop back to BUILD.

---

## Phase 5: DOCUMENT
**Goal**: Keep documentation in sync with code.

### 5.1 Docstrings
// turbo
   - `/write_docstrings`
   - **Target**: New methods with Google-style docstrings.

### 5.2 Update Guides
// turbo
   - `/update_docs`
   - **Update**:
     - `docs/guides/usage.md` — add usage examples
     - `README.md` — update if Quick Start affected
     - `examples/` — add example script if helpful

### 5.3 Update Goals
   - **File**: `AUTOMATION_GOALS.md`
   - **Action**: Mark workflow as completed (W1-W6 checkboxes).

### 5.4 Update Roadmap
   - **File**: `docs/development/roadmap.md`
   - **Action**: Check off completed feature, add new ideas if discovered.

---

## Phase 6: RELEASE
**Goal**: Ship the feature.

### 6.1 Prepare Release
// turbo
   - `/release_prep`
   - **Actions**:
     - Bump version in `pyproject.toml`
     - Update `CHANGELOG.md`
     - Git commit and tag

### 6.2 Final Verification
// turbo
   - `python scripts/smoke_test.py all`
   - **Gate**: Must pass before push.

### 6.3 Push to Origin
   - `git push origin main --tags`

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

| Phase | Workflows Called |
|-------|-----------------|
| 1. ANALYZE | `/health_check`, `/coverage_audit`, `/propose_features`, `/ideate_innovations` |
| 2. PLAN | *User interaction* |
| 3. BUILD | `/scaffold_new_script`, `/cross_service_builder` |
| 4. VERIFY | `/development`, `/ci_local`, `/verify_installation`, `/bootstrap_tests` |
| 5. DOCUMENT | `/write_docstrings`, `/update_docs` |
| 6. RELEASE | `/release_prep` |
