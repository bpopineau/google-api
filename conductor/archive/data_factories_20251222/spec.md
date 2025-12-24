# Specification: Deterministic Data Factories

## Overview
This feature introduces a suite of data factories using `polyfactory` to generate type-safe, predictable mock data for Google API resources. These factories will simplify unit testing by eliminating the need to manually construct complex dictionaries and ensuring mock data always adheres to the project's `TypedDict` definitions.

## Functional Requirements

### 1. Library Selection
- Use `polyfactory` as the underlying engine for all data generation.
- Factories must be compatible with `TypedDict` definitions in `mygooglib/core/types.py`.

### 2. Factory Organization
- Place factory definitions in a new `tests/factories/` directory.
- Use submodules mirroring the service structure:
    - `tests/factories/drive.py`
    - `tests/factories/sheets.py`
    - `tests/factories/gmail.py`
    - `tests/factories/common.py` (for library-specific types)

### 3. Core Resource Coverage
Implement factories for the following `TypedDict` models:
- **Drive:** `FileDict`
- **Sheets:** `SpreadsheetDict`, `SheetDict`, `ValueRangeDict`
- **Gmail:** `MessageDict`, `ThreadDict`, `LabelDict`
- **Library Normalized:** `SheetInfoDict`, `MessageMetadataDict`, `MessageFullDict`, `AttachmentMetadataDict`

### 4. Deterministic Defaults
- Factories should provide sensible, deterministic defaults (e.g., standard MIME types, valid-looking IDs).
- Support overrides for any field to test edge cases (e.g., empty lists, null values, specific dates).

## Non-Functional Requirements
- **Test-Only Dependency:** `polyfactory` should be added as a development dependency (`dev` group in `pyproject.toml`).
- **Zero Runtime Impact:** Factories must not be imported or required by the production `mygooglib` package.

## Acceptance Criteria
- [ ] `polyfactory` is added to `pyproject.toml` (dev dependencies).
- [ ] `FileFactory.build()` returns a valid `FileDict` dictionary.
- [ ] Overriding values (e.g., `FileFactory.build(name="custom.txt")`) works as expected.
- [ ] Factories are successfully used in at least one unit test to replace a manually defined dictionary.

## Out of Scope
- Factories for services not yet implemented in the core library (e.g., Calendar, Tasks).
- Mocking the actual Google API client/discovery logic (this is for data generation only).
