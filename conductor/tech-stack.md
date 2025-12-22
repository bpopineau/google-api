# Tech Stack: MyGoog

## Core Technologies
- **Programming Language:** Python (>=3.10)
- **GUI Framework:** PySide6 (Qt for Python) - Used for building the desktop application with a modern, responsive UI.
- **CLI Framework:** Typer & Rich - Used for creating a powerful and visually appealing command-line interface.

## Google Workspace Integration
- **API Client:** `google-api-python-client` - The official library for interacting with Google APIs.
- **Services:** Drive, Gmail, Calendar, Sheets, Tasks.
- **Authentication:** `google-auth-oauthlib` - Handles OAuth2 flow and credential management.

## Development & Quality Assurance
- **Testing:** Pytest (including `pytest-qt` for UI testing).
- **Linting & Formatting:** Ruff.
- **Static Type Checking:** Mypy.
- **Environment Management:** `pyproject.toml` (standardized build and dependency management).

## Data Processing
- **Pandas:** (Optional) Included for handling complex data manipulations between local files and Google Sheets.


