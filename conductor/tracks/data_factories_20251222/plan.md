# Plan: Deterministic Data Factories

Implementation of type-safe, deterministic mock data generators using `polyfactory` for use in unit tests.

## Phase 1: Environment and Foundation
- [x] Task: Add `polyfactory` to `pyproject.toml` (dev-dependencies) and install. 2d6b769
- [x] Task: Create directory structure: `tests/factories/` with `__init__.py`. 7ed1498
- [x] Task: Implement `tests/factories/common.py` for shared types and library-specific normalized dicts. 710240d
- [ ] Task: Conductor - User Manual Verification 'Environment and Foundation' (Protocol in workflow.md)

## Phase 2: Drive and Sheets Factories
- [ ] Task: Implement `tests/factories/drive.py` (FileDict, etc.).
- [ ] Task: Implement `tests/factories/sheets.py` (ValueRangeDict, SpreadsheetDict, etc.).
- [ ] Task: Write tests in `tests/utils/test_factories_basic.py` to ensure factories generate valid types.
- [ ] Task: Conductor - User Manual Verification 'Drive and Sheets Factories' (Protocol in workflow.md)

## Phase 3: Gmail Factories
- [ ] Task: Implement `tests/factories/gmail.py` (MessageDict, ThreadDict, etc.).
- [ ] Task: Update `tests/utils/test_factories_basic.py` with Gmail factory tests.
- [ ] Task: Conductor - User Manual Verification 'Gmail Factories' (Protocol in workflow.md)

## Phase 4: Integration and Refactoring
- [ ] Task: Identify 2-3 existing tests using hardcoded dictionaries (e.g., in Drive or Sheets services).
- [ ] Task: Refactor identified tests to use the new factories.
- [ ] Task: Verify all tests pass and coverage is maintained.
- [ ] Task: Conductor - User Manual Verification 'Integration and Refactoring' (Protocol in workflow.md)
