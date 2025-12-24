# Specification: Systematic Type Fixing (Zero Mypy Errors)

## 1. Overview
This track aims to resolve all 240+ identified `mypy` errors across the repository to achieve a "clean build" state. By enforcing strict type safety, we reduce ambiguity for both human developers and AI agents (as per `ai_ergonomics.md`), ensuring that types propagate correctly from the core library up to the application layers.

## 2. Functional Requirements
- **Goal:** Reduce `mypy` error count to 0.
- **Scope:** All Python files in `mygooglib`, `mygoog_cli`, and `mygoog_gui`.
- **Strategy:** Fix errors in dependency order to prevent error propagation and rework.
    1.  **Foundation:** `mygooglib/core`
    2.  **Services:** `mygooglib/services` (Apply existing schemas for Sheets/Gmail/Drive; create new schemas for Calendar/Tasks/Contacts/Docs)
    3.  **CLI:** `mygoog_cli`
    4.  **GUI:** `mygoog_gui`

## 3. Detailed Execution Plan
1.  **Phase 1: Foundation (`mygooglib/core`)**
    -   Resolve the ~8 errors in the core utilities.
    -   Ensure base types and configurations are strictly typed.

2.  **Phase 2: Services (`mygooglib/services`)**
    -   **Sub-phase A: Existing Schemas:** Apply defined `TypedDict` schemas from `mygooglib/core/types.py` to `sheets.py`, `gmail.py`, and `drive.py`.
    -   **Sub-phase B: New Schemas:** Define missing `TypedDict` schemas for `calendar.py`, `tasks.py`, `contacts.py`, and `docs.py` and apply them.

3.  **Phase 3: Application Logic (`mygoog_cli`)**
    -   Resolve ~36 errors in the CLI layer.
    -   Verify that library types are correctly consumed by the CLI commands.

4.  **Phase 4: Presentation Layer (`mygoog_gui`)**
    -   Resolve ~68 errors in the PySide6 GUI code.
    -   Address specific GUI typing challenges (e.g., Qt signals/slots, widget hierarchies).

## 5. Acceptance Criteria
-   Running `uv run mypy .` (or `mypy .`) returns `Success: no issues found`.
-   No `type: ignore` comments are added unless absolutely necessary and documented with a specific justification (e.g., upstream library bug).
-   `TypedDict` schemas are defined and used for all Google API resource objects (Calendar events, Tasks, etc.).
