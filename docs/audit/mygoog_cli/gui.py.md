# Audit Report: mygoog_cli/gui.py

## Purpose
- Provides a simple CLI bridge to launch the PySide6 desktop application via the `mg gui run` command.

## Main Exports
- `run_gui`: Command function that imports and executes the GUI's main loop.

## Findings
- **Dependency Management:** Correctly implements a `try-except ImportError` block. This is vital because PySide6 is a large dependency and is treated as an optional extra (`pip install mygooglib[gui]`). The error message provides clear installation instructions.
- **Lazy Loading:** By importing `mygoog_gui.main` only inside the command function, the module avoids overhead for users who only want to use the CLI.

## Quality Checklist
- [x] Handles missing GUI dependencies gracefully
- [x] Provides clear installation instructions in case of failure
- [x] Minimal overhead for non-GUI users
