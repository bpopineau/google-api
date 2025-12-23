# Audit Report: mygoog_cli/main.py

## Purpose
- The primary orchestrator for the `mg` command-line application. It aggregates all sub-commands, manages global flags, initializes the shared application state, and provides centralized error handling.

## Main Exports
- `main()`: The top-level entry point function that executes the Typer application and catches global exceptions.
- `_global_options`: Callback function that processes flags like `--debug`, `--json`, and path overrides.

## Findings
- **Aggregation Logic:** Successfully integrates over a dozen sub-command modules into a unified command hierarchy, providing a consistent "Personal Google Automation" interface.
- **Global State Management:** Properly initializes `CliState` and calls `configure_environment`, ensuring that global configuration is available to all sub-commands and propagates down to the library layer.
- **User-Centric Error Handling:** The catch-all logic in `main()` for `GoogleApiError` and other expected failures ensures that users receive readable error panels instead of raw Python tracebacks, unless `--debug` is explicitly requested.
- **Rich Integration:** Correctly installs `rich.traceback` when debugging, enhancing the developer experience for troubleshooting.

## Quality Checklist
- [x] All sub-commands are correctly registered
- [x] Global options propagate to the library layer correctly
- [x] Global error handling is robust and user-friendly
