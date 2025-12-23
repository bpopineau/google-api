# mygoog_cli

## Purpose
Provides the Command-Line Interface (CLI) for the application. It exposes services and workflows as executable commands using `typer` for argument parsing and `rich` for formatted output. This is the primary interface for power users and automation.

## Key Entry Points
- [`main.py`](file:///c:/Users/brand/Projects/google-api/mygoog_cli/main.py): All CLI commands are registered and organized here. It serves as the central router for the `mg` command.
- [`cli_entry.py`](file:///c:/Users/brand/Projects/google-api/mygoog_cli/cli_entry.py): The setuptools entry point script that bootstraps the Typer application.
- [`dev.py`](file:///c:/Users/brand/Projects/google-api/mygoog_cli/dev.py): Development-specific commands (e.g., scaffolding, testing helpers) hidden from standard users.

## Dependencies
- **External:** `typer`, `rich`
- **Internal:** `mygooglib` (consumes core logic and services)
