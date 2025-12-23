# Specification: Ergonomics - Strict Schemas for Sheets & Gmail

## Overview
This track aims to significantly enhance developer ergonomics and AI agent effectiveness by introducing strict typing for Google API responses. Currently, the library returns loose `dict` or `list[dict]` objects, which forces developers and agents to guess field names (e.g., `mimeType` vs `mime_type`) and leads to runtime errors. By implementing `TypedDict` schemas, we provide an explicit contract for API data.

## Functional Requirements
1. **Schema Definition**:
    - Create a central registry in `mygooglib/core/types.py`.
    - Implement standard Python `TypedDict` models for the most common response shapes in the **Sheets** and **Gmail** services.
    - Set `total=False` on `TypedDict` definitions to account for the optional nature of many Google API response fields.

2. **Library Integration**:
    - Update return type annotations in `mygooglib/services/sheets.py` and `mygooglib/services/gmail.py` to use the new `TypedDict` schemas instead of generic `dict`.
    - Ensure all public-facing methods in these services are fully typed according to the new schemas.

3. **Discoverability**:
    - Re-export high-value schemas in `mygooglib/__init__.py` for easy access by library users.
    - Regenerate the Context Map (`conductor/context_map.md`) to reflect the new strict types.

## Non-Functional Requirements
- **Zero Runtime Overhead**: Use `typing.TypedDict` which has no impact on execution speed or memory compared to standard dicts.
- **Dependency-Free**: Do not add new libraries (like Pydantic) to the core project.
- **Strict mypy Compliance**: All new types must pass existing `mypy` strict checks as configured in `pyproject.toml`.

## Acceptance Criteria
- [ ] `mygooglib/core/types.py` exists and contains schemas for Sheets (e.g., `SpreadsheetDict`, `SheetDict`, `ValueRangeDict`) and Gmail (e.g., `MessageDict`, `ThreadDict`, `LabelDict`).
- [ ] `mygooglib/services/sheets.py` method signatures are updated and pass `mypy --disallow-untyped-defs`.
- [ ] `mygooglib/services/gmail.py` method signatures are updated and pass `mypy --disallow-untyped-defs`.
- [ ] `pytest` suite passes 100% without regression.
- [ ] `conductor/context_map.md` is updated and lists the new typed signatures.

## Out of Scope
- Runtime validation of API responses (no Pydantic validation).
- Typing for Drive, Calendar, Tasks, or AppScript (reserved for Phase 2/3).
- Refactoring internal logic to classes (keeping the current dict-based internal logic, only typing the interfaces).
