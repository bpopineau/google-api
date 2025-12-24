# Specification: Pragmatic API Response Schemas

## 1. Overview
This track extends the existing `TypedDict` schemas in `mygooglib/core/types.py` to cover additional Google Workspace APIs. We adopt the "Pragmatic Subset" approach: defining types only for fields actively used by our application.

## 2. Goals
*   **Explicit Contracts:** Define clear `TypedDict` structures for key API responses.
*   **AI Ergonomics:** Provide clean, clutter-free schema reference for AI agents.
*   **Type Safety:** Enable strict `mypy` checking for API interactions.
*   **Consistency:** All services follow the same typing pattern.

## 3. Scope
### 3.1 Services to Add
*   **Calendar:** Events, Calendars (CalendarListEntry).
*   **Tasks:** TaskLists, Tasks.
*   **Contacts:** People, Connections.
*   **Docs:** Documents.

### 3.2 Already Complete (Out of Scope)
*   **Sheets:** Already typed in `core/types.py`
*   **Drive:** Already typed in `core/types.py`
*   **Gmail:** Already typed in `core/types.py`

### 3.3 Data Direction
*   **Response Bodies Only:** Focus on Read operations (GET/LIST).
*   **Request Bodies:** Out of scope for this track.

## 4. Technical Approach
### 4.1 Schema Definition
*   **Type:** `TypedDict` (using `typing.TypedDict`).
*   **Location:** `mygooglib/core/types.py` (extend existing file).
*   **Philosophy:** "Pragmatic Subset" - include only fields used by `mygooglib` logic. Omit verbose metadata (e.g., `etag`, `kind`, `selfLink`) unless needed.
*   **Runtime Behavior:** "Pure Hinting" - use `cast` or type hints. Raw API response remains intact.

### 4.2 Verification Strategy
1.  **Static Analysis:** `mypy` must pass without errors.
2.  **Contract Tests:** Tests in `tests/core/test_types_contract.py` that assert defined schema fields exist in real API responses.

## 5. Acceptance Criteria
*   [ ] `TypedDict`s added to `core/types.py` for Calendar, Tasks, Contacts, Docs.
*   [ ] Service modules updated to use these types for return values.
*   [ ] `mypy` runs clean on all updated files.
*   [ ] Contract tests verify defined schema fields exist in real API responses.
*   [ ] New types re-exported from `mygooglib/__init__.py`.
