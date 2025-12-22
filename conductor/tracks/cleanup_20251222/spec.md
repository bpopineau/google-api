# Track Specification: Repo Cleanup

## Overview
This track focuses on cleaning up the repository by removing unused files and directories. This is a maintenance chore to keep the codebase clean and reduce noise.

## Requirements

### Functional
1.  **File Removal:** The following files and directories must be permanently deleted:
    -   `.streamlit/` (directory)
    -   `mygooglib/cli/` (directory)
    -   `mygooglib/gui/` (directory)
    -   `test_temp.md` (file)
    -   `pytest_output.txt` (file)

2.  **Verification:**
    -   The application must pass all standard tests (`pytest`).
    -   The CLI entry point must function correctly (`mg --help`).
    -   The GUI package must be importable (`python -c "import mygoog_gui.main; print('GUI import successful')"`).
    -   Codebase must be free of linting errors (`ruff check .`).
    -   Codebase must pass type checking (`mypy .`).

### Non-Functional
1.  **Safety:** Ensure no active code or configuration is accidentally removed.

## Out of Scope
*   Refactoring code within the remaining files.
*   Updating dependencies.
