# Implementation Plan - Pragmatic API Response Schemas

> **Note:** Types already exist in `mygooglib/core/types.py` with Sheets, Drive, and Gmail schemas. This plan extends that file rather than creating a parallel `services/schemas/` package.

## Phase 1: Calendar & Tasks Types [checkpoint: b0b3b18]
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
- [x] Task: Conductor - Phase 1 Verification

## Phase 2: Contacts & Docs Types [checkpoint: b1acf44]
Add TypedDicts for services with complex/nested structures.

- [x] Task: Implement Contacts Types [b1acf44]
    - [x] Add `ContactDict` (Pragmatic Subset) to `core/types.py`
    - [x] Update `mygooglib/services/contacts.py` return type hints
    - [x] Add contract tests
- [x] Task: Implement Docs Types [b1acf44]
    - [x] Add `DocumentDict` (Pragmatic Subset) to `core/types.py`
    - [x] Add contract tests
- [x] Task: Conductor - Phase 2 Verification

## Phase 3: Final Polish
Ensure comprehensive coverage and validation.

- [x] Task: Full Suite Verification
    - [x] Run full `mypy` check
    - [x] Run full test suite (unit + contract)
- [x] Task: Re-export new types from `mygooglib/__init__.py`
- [x] Task: Conductor - Final Verification
