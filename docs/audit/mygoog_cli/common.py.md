# Audit Report: mygoog_cli/common.py

## Purpose
- Contains shared utilities, classes, and state management logic for the entire CLI application. Ensures consistency in output formatting, error handling, and environment configuration.

## Main Exports
- `CliState`: Dataclass holding the global CLI configuration and Rich console instances.
- `configure_environment`: Propagates CLI flags (paths, debug) to the library layer via environment variables.
- `format_output`: Centralizes the logic for switching between human-readable text and JSON output.
- `prompt_selection`: A robust, reusable interactive selection prompt for list-based data.
- Styling helpers: `print_error`, `print_success`, `print_kv`.

## Findings
- **Architectural Integrity:** The use of `CliState` and `from_ctx` is a very mature pattern for Typer applications, ensuring that global state is handled safely without relying on global variables.
- **Environment Propagation:** Correctly bridges the CLI and Library layers by setting environment variables (`MYGOOGLIB_*`), ensuring that library components (like `auth.py`) respect CLI-level path overrides.
- **UI Consistency:** Standardizing error and success messages via common helpers ensures a professional, unified look across all commands.

## Quality Checklist
- [x] State management is clean and robust
- [x] Environment propagation is correct
- [x] UI helpers provide consistent styling
