# Audit Report: mygoog_cli/cli_entry.py

## Purpose
- Serves as the primary entry point for the entire application (`mg` command). Responsible for dispatching the user to either the Graphical User Interface (GUI) or the Command Line Interface (CLI) based on the provided arguments.

## Main Exports
- `main()`: The dispatch function.

## Findings
- **Smart Dispatch:** Implements a sensible default where running the command without arguments launches the GUI, which is friendly for casual users.
- **Explicit Override:** Provides `--gui` and `-g` flags for users who want to be certain they launch the GUI even if arguments are technically present (though not currently used by the heuristic).
- **Separation of Concerns:** Does not contain any business logic; it acts purely as a router, keeping the entry point lightweight.

## Quality Checklist
- [x] Heuristics for mode switching are clear
- [x] CLI/GUI imports are lazy-loaded within the functions
- [x] Exit codes are handled correctly
