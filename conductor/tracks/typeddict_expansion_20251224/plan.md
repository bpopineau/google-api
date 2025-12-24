# Implementation Plan - Pragmatic API Response Schemas

> **Note:** Types already exist in `mygooglib/core/types.py` with Sheets, Drive, and Gmail schemas. This plan extends that file rather than creating a parallel `services/schemas/` package.

## Phase 1: Calendar & Tasks Types
Add TypedDicts for the simpler productivity services.

- [x] Task: Implement Calendar Types [f5f0d56]
    - [x] Add `CalendarEvent`, `CalendarListEntry` to `core/types.py`
    - [x] Update `mygooglib/services/calendar.py` return type hints
    - [x] Run `mypy` to verify
- [x] Task: Implement Tasks Types [f5f0d56]
    - [x] Add `Task`, `TaskList` to `core/types.py`
    - [x] Update `mygooglib/services/tasks.py` return type hints
    - [x] Run `mypy` to verify
- [x] Task: Add Contract Tests for Phase 1 [f5f0d56]
    - [x] Create `tests/test_types_contract.py` with helper logic
    - [x] Add Calendar/Tasks contract assertions
- [ ] Task: Conductor - Phase 1 Verification

## Phase 2: Contacts & Docs Types
Add TypedDicts for services with complex/nested structures.

- [ ] Task: Implement Contacts Types
    - [ ] Add `Person`, `Connection` (Pragmatic Subset) to `core/types.py`
    - [ ] Update `mygooglib/services/contacts.py` return type hints
    - [ ] Add contract tests
- [ ] Task: Implement Docs Types
    - [ ] Add `Document` (Pragmatic Subset) to `core/types.py`
    - [ ] Update `mygooglib/services/docs.py` return type hints
    - [ ] Add contract tests
- [ ] Task: Conductor - Phase 2 Verification

## Phase 3: Final Polish
Ensure comprehensive coverage and validation.

- [ ] Task: Full Suite Verification
    - [ ] Run full `mypy` check
    - [ ] Run full test suite (unit + contract)
    - [ ] Update `context_map.md` to reflect new types
- [ ] Task: Re-export new types from `mygooglib/__init__.py`
- [ ] Task: Conductor - Final Verification
