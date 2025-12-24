# Plan: Deterministic Data Factories

Implementation of type-safe, deterministic mock data generators using `polyfactory` for use in unit tests.

## Phase 1: Environment and Foundation [checkpoint: e586488]
- [x] Task: Add `polyfactory` to `pyproject.toml` (dev-dependencies) and install. 2d6b769
- [x] Task: Create directory structure: `tests/factories/` with `__init__.py`. 7ed1498
- [x] Task: Implement `tests/factories/common.py` for shared types and library-specific normalized dicts. 710240d
- [x] Task: Conductor - User Manual Verification 'Environment and Foundation' (Protocol in workflow.md) e586488

## Phase 2: Drive and Sheets Factories [checkpoint: b812ecb]
- [x] Task: Implement `tests/factories/drive.py` (FileDict, etc.). d3d529f
- [x] Task: Implement `tests/factories/sheets.py` (ValueRangeDict, SpreadsheetDict, etc.). ffb65ba
- [x] Task: Write tests in `tests/utils/test_factories_basic.py` to ensure factories generate valid types. 86dbc09
- [x] Task: Conductor - User Manual Verification 'Drive and Sheets Factories' (Protocol in workflow.md) b812ecb

## Phase 3: Gmail Factories [checkpoint: a9728f6]
- [x] Task: Implement `tests/factories/gmail.py` (MessageDict, ThreadDict, etc.). 5b3da0c
- [x] Task: Update `tests/utils/test_factories_basic.py` with Gmail factory tests. 5b3da0c
- [x] Task: Conductor - User Manual Verification 'Gmail Factories' (Protocol in workflow.md) a9728f6

## Phase 4: Integration and AI Ergonomics Compliance
- [ ] Task: Identify 2-3 existing tests using hardcoded dictionaries (e.g., in Drive or Sheets services).
- [ ] Task: Refactor identified tests to use the new factories.
- [ ] Task: Verify AI Ergonomics compliance:
    - [ ] Sub-task: Run `uv run mypy tests/factories/` - ensure 0 errors
    - [ ] Sub-task: Run `uv run ruff check tests/factories/` - ensure no linting errors
    - [ ] Sub-task: Verify all factory classes have docstrings
- [ ] Task: Verify all tests pass and coverage is maintained.
- [ ] Task: Conductor - User Manual Verification 'Integration and AI Ergonomics' (Protocol in workflow.md)
