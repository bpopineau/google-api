# Specification: Project Reorganization (Track: project-organization)

## Overview
This track aims to improve the maintainability and scalability of the MyGoog project by establishing clear boundaries between the core library, the CLI, and the GUI. The goal is to create a modular structure that allows for independent usage of the core library while providing well-defined entry points for user interfaces.

## Functional Requirements
- **Unified Dependency Management:** Use a single `pyproject.toml` with "extras" to manage dependencies for `mygooglib`, `mygoog_cli`, and `mygoog_gui`.
- **Global Configuration:** Migrate configuration and credentials (e.g., `token.json`, `credentials.json`) from the project root to a user-specific directory (`~/.mygoog/`).
- **Clean Namespace:** Reorganize `mygooglib` to expose a high-level public API while hiding internal implementation details and utilities.
- **Entry Points:**
    - `mg`: Command-line interface.
    - `mgui`: Graphical user interface.

## Technical Requirements
- **Package Layout:**
    - `mygooglib/`: Core library (Drive, Gmail, Sheets, etc.).
        - `core/`: Internal utilities (logging, retry, auth, pagination).
        - `services/`: Low-level service implementations.
        - `workflows/`: High-level automation logic.
    - `mygoog_cli/`: CLI implementation, depending on `mygooglib`.
    - `mygoog_gui/`: GUI implementation (PySide6), depending on `mygooglib`.
- **Public API:** Standardize `mygooglib/__init__.py` to re-export primary service classes and workflow entry points for cleaner imports.
- **Migration Path:** Provide clear migration notes in `CHANGELOG.md` for breaking import changes.

## Acceptance Criteria
- [ ] `mygooglib` can be installed and used as a standalone library without GUI dependencies.
- [ ] `mg` command launches the CLI and operates correctly using config from `~/.mygoog/`.
- [ ] `mgui` command launches the GUI and operates correctly.
- [ ] All existing tests pass after updating to new import paths.
- [ ] `python scripts/smoke_test.py all` passes.
- [ ] Code coverage for `mygooglib` remains >80%.

## Out of Scope
- Adding new features to Google API services.
- Major behavioral changes to existing automation logic.

