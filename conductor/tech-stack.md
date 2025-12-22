# Technology Stack - MyGoog (mg)

## Core Technologies
*   **Programming Language:** Python >= 3.10
*   **Package Manager:** `uv` (for fast dependency resolution and management)
*   **GUI Framework:** PySide6 (Qt for Python) - Chosen for native performance and instant startup responsiveness.
*   **CLI Framework:** Typer + Rich - Used for beautiful, self-documenting command-line interfaces.

## Google Integration
*   **Core Libraries:**
    *   `google-api-python-client`: Primary interface for Google Workspace APIs.
    *   `google-auth` / `google-auth-oauthlib`: Robust OAuth2 authentication management.

## Data & Utilities
*   **Optional Libraries:**
    *   `pandas`: Utilized for advanced data handling and manipulation when needed.

## Development & Quality Assurance
*   **Testing:** `pytest` (including `pytest-qt` for GUI testing)
*   **Linting & Formatting:** `ruff` - Providing high-quality code checks with minimal configuration.
*   **Type Checking:** `mypy` - Ensuring long-term maintainability through strict type safety.

## Project Structure & Entry Points
*   **Desktop App:** `mgui` (Entry point: `mygoog_gui.main:main`)
*   **CLI Tool:** `mg` (Entry point: `mygoog_cli.main:main`)
*   **Library:** `mygooglib` (Core logic and API wrappers)
