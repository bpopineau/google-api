# Specification: Unified Debug Console (REPL)

## Overview
This feature introduces a pre-configured interactive Python environment (`mg console`) powered by IPython. It simplifies debugging and experimentation by automatically handling authentication, initializing API clients, and importing all core library types and services, allowing agents and developers to interact with Google Workspace data instantly.

## Functional Requirements

### 1. CLI Integration
- Add a `console` command to the `mg` (Typer) CLI.
- The command should:
    - Load the project configuration and credentials.
    - Initialize the Google API service clients (Drive, Sheets, Gmail, etc.).
    - Launch an IPython interactive session.

### 2. Auto-Imports (The "Context")
The following should be available in the global namespace of the REPL:
- **Clients:** `drive`, `sheets`, `gmail`, `calendar`, `tasks` (already authenticated).
- **Services:** `drv`, `sht`, `gml`, `cal`, `tsk` (aliases to the service modules).
- **Types:** All `TypedDict` definitions from `mygooglib.core.types`.
- **Utils:** `get_logger`, `get_config`.

### 3. Environment Features
- Use `IPython` for the REPL environment to provide:
    - Tab completion for all API methods and types.
    - Syntax highlighting.
    - Persistent history across sessions.

## Non-Functional Requirements
- **Interactive Focus:** The console is a development/debugging tool and should not be used for production automation scripts.
- **Dependency Management:** `ipython` should be added as a development dependency.

## Acceptance Criteria
- [ ] `ipython` is added to `pyproject.toml` (dev dependencies).
- [ ] Running `mg console` opens an interactive IPython shell.
- [ ] Inside the shell, `drive.files().list().execute()` (or similar) works without any setup.
- [ ] All `TypedDict` definitions are available (e.g., `FileDict`).

## Out of Scope
- A custom GUI console (CLI only for now).
- Automatic modification of live production data without confirmation (Standard Python rules apply; use at your own risk).
