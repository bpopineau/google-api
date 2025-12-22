# Implementation Plan: Ergonomics - Strict Schemas

## Phase 1: Setup & Basic Types [checkpoint: 2975e91]
Define the central registry and the first set of foundational schemas.

- [x] Task: Create Type Registry [e9fc118]
    - [x] Sub-task: Create `mygooglib/core/types.py`
    - [x] Sub-task: Define basic shared types (e.g., `DateDict`, `ColorDict`)
- [x] Task: Define Sheets Foundational Types [e9fc118]
    - [x] Sub-task: Define `ValueRangeDict` (for range values)
    - [x] Sub-task: Define `SpreadsheetDict` and `SheetDict` (for metadata)
- [x] Task: Verify Phase 1 Types [e9fc118]
    - [x] Sub-task: Write unit tests in `tests/utils/test_types.py` that instantiate these TypedDicts with valid/invalid data
    - [x] Sub-task: Run `uv run mypy mygooglib/core/types.py`
- [x] Task: Conductor - User Manual Verification 'Setup & Basic Types' [2975e91]

## Phase 2: Sheets Service Integration
Integrate the new types into the Sheets service and enforce strict typing.

- [~] Task: Red Phase - Sheets Typings
    - [ ] Sub-task: Update `mygooglib/services/sheets.py` with import from `mygooglib.core.types`
    - [ ] Sub-task: Change return type annotations to the new `TypedDicts`
    - [ ] Sub-task: Run `uv run mypy mygooglib/services/sheets.py` and confirm failures (Red)
- [ ] Task: Green Phase - Resolve Sheets Type Errors
    - [ ] Sub-task: Fix any logic or annotation mismatches in `sheets.py` to satisfy mypy
    - [ ] Sub-task: Run `pytest tests/test_sheets_exists.py` (and other sheets tests) to ensure zero regressions
- [ ] Task: Conductor - User Manual Verification 'Sheets Service Integration' (Protocol in workflow.md)

## Phase 3: Gmail Service Integration
Integrate the new types into the Gmail service.

- [ ] Task: Define Gmail Foundational Types
    - [ ] Sub-task: Define `MessageDict`, `ThreadDict`, and `LabelDict` in `types.py`
- [ ] Task: Red Phase - Gmail Typings
    - [ ] Sub-task: Update `mygooglib/services/gmail.py` with new type annotations
    - [ ] Sub-task: Run `uv run mypy mygooglib/services/gmail.py` and confirm failures (Red)
- [ ] Task: Green Phase - Resolve Gmail Type Errors
    - [ ] Sub-task: Fix mismatches in `gmail.py`
    - [ ] Sub-task: Run `pytest tests/test_gmail_attachments.py` to ensure zero regressions
- [ ] Task: Conductor - User Manual Verification 'Gmail Service Integration' (Protocol in workflow.md)

## Phase 4: Finalization & AI Context Map
Expose types to the public API and update the agent "cheat sheet".

- [ ] Task: Public API Export
    - [ ] Sub-task: Re-export core types in `mygooglib/__init__.py`
- [ ] Task: Update Context Map
    - [ ] Sub-task: Run `python scripts/generate_context_map.py`
    - [ ] Sub-task: Verify `conductor/context_map.md` shows the new strict signatures
- [ ] Task: Conductor - User Manual Verification 'Finalization & AI Context Map' (Protocol in workflow.md)
