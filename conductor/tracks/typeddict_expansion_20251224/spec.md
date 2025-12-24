# Specification: Pragmatic API Response Schemas

## 1. Overview
This track aims to improve type safety and AI ergonomics by implementing `TypedDict` schemas for Google Workspace API responses. We will adopt a "Pragmatic Subset" approach, defining types only for the fields actively used by our application, rather than mirroring the exhaustive Google API schema. These schemas will reside in a dedicated `mygooglib/services/schemas/` package.

## 2. Goals
*   **Explicit Contracts:** Define clear `TypedDict` structures for key API responses.
*   **AI Ergonomics:** Provide a clean, clutter-free schema reference for AI agents to understand data structures.
*   **Type Safety:** enable strict `mypy` checking for API interactions.
*   **Consistency:** Retrofit the existing Gmail service to match this new pattern.

## 3. Scope
### 3.1 Services Covered
*   **Calendar:** Events, Calendars.
*   **Tasks:** TaskLists, Tasks.
*   **Contacts:** People, Connections.
*   **Docs:** Documents.
*   **Gmail:** Retrofit Messages, Threads, Labels, Drafts (aligning with new pattern).

### 3.2 Data Direction
*   **Response Bodies Only:** Focus on Read operations (GET/LIST).
*   **Request Bodies:** Out of scope for this track.

## 4. Technical Approach
### 4.1 Schema Definition
*   **Type:** `TypedDict` (using `typing.TypedDict`).
*   **Location:** `mygooglib/services/schemas/<service_name>.py`.
*   **Philosophy:** "Pragmatic Subset" - include only fields used by `mygooglib` logic or likely to be used. Omit verbose, unused metadata (e.g., `etag`, `kind`, `selfLink` unless specifically needed).
*   **Runtime Behavior:** "Pure Hinting" - We will use `cast` or type hints. We will **NOT** strip data at runtime. The raw API response remains intact; our types just describe the subset we care about.

### 4.2 Directory Structure
```text
mygooglib/
├── services/
│   ├── schemas/          # NEW PACKAGE
│   │   ├── __init__.py
│   │   ├── gmail.py
│   │   ├── calendar.py
│   │   ├── tasks.py
│   │   ├── contacts.py
│   │   └── docs.py
```

### 4.3 Verification Strategy
1.  **Static Analysis:** `mypy` must pass without errors.
2.  **Contract Tests:** New tests in `tests/schemas/` that reuse existing VCR cassettes (or new live calls) to assert that the keys defined in our `TypedDict`s actually exist in the raw API responses.

##  acceptance Criteria
*   [ ] `mygooglib/services/schemas/` package created.
*   [ ] `TypedDict`s defined for Calendar, Tasks, Contacts, Docs, and Gmail responses.
*   [ ] Service modules updated to import and use these types for return values.
*   [ ] `mypy` runs clean on all updated files.
*   [ ] Contract tests verify that defined schema fields exist in real API responses.
