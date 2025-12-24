# Plan: Systematic Type Fixing (Zero Mypy Errors)

## Phase 1: Foundation (`mygooglib/core`) [checkpoint: completed]
- [x] Task: Resolve mypy errors in `mygooglib/core/` *(0 errors found - already clean)*
    - [x] Run `mypy mygooglib/core` to identify current errors.
    - [x] ~~Fix type hints~~ (No fixes needed)
    - [x] Verify fix by running `mypy mygooglib/core`.
- [x] Task: Verify Core Unit Tests
    - [x] Run `uv run pytest tests/test_config.py tests/test_auth.py` to ensure no regressions.
- [x] Task: Conductor - User Manual Verification 'Foundation' *(Skipped - no changes needed)*

## Phase 2: Services Part A (Existing Schemas) [checkpoint: completed]
- [x] Task: Apply TypedDict schemas to Sheets Service *(Already applied, 0 errors)*
- [x] Task: Apply TypedDict schemas to Gmail Service *(Already applied, 0 errors)*
- [x] Task: Apply TypedDict schemas to Drive Service *(Already applied, 0 errors)*
- [x] Task: Verify Service Unit Tests (Part A)

## Phase 3: Services Part B (New Schemas) [checkpoint: completed]
- [x] Task: Define and apply schemas for Calendar *(Already applied, 0 errors)*
- [x] Task: Define and apply schemas for Tasks *(Already applied, 0 errors)*
- [x] Task: Define and apply schemas for Contacts & Docs *(Already applied, 0 errors)*
- [x] Task: Verify Service Unit Tests (Part B)

## Phase 4: Application Logic (`mygoog_cli`) [checkpoint: completed]
- [x] Task: Resolve mypy errors in `mygoog_cli/`
    - Fixed 10 `dict-item` errors in `console.py` by adding explicit `dict[str, Any]` type annotation
- [x] Task: Verify CLI Unit Tests

## Phase 5: Presentation Layer (`mygoog_gui`) [checkpoint: completed]
- [x] Task: Resolve mypy errors in `mygoog_gui/` *(0 errors found - already clean)*
- [x] Task: Verify GUI Unit Tests

## Phase 6: Final Integration & Cleanup [checkpoint: completed]
- [x] Task: Global Mypy Verification
    - `uv run mypy .` → **Success: no issues found in 123 source files**
- [x] Task: Full Test Suite Execution
    - `uv run pytest` → **156 passed in 1.45s**
- [x] Task: Quality Gates
    - Ruff: All checks passed
    - Architecture linter: 3 contracts kept, 0 broken
- [x] Task: Additional fix in test factories
    - Fixed `var-annotated` error in `tests/factories/common.py` by adding `list[AttachmentMetadataDict]` type

## Summary

**Before:** 240+ mypy errors reported (from ai_ergonomics.md audit)
**After:** 0 mypy errors in 123 source files

**Files Modified:**
1. `mygoog_cli/console.py` - Added explicit `dict[str, Any]` type for service_shortcuts
2. `tests/factories/common.py` - Added type annotation for `attachments` field
3. `tests/cli/test_console.py` - Added `noqa: F401` for intentional import test
