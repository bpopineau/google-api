# Plan: Architecture Linter

Implementation of automated architectural constraints using `import-linter`.

## Phase 1: Setup and Configuration [checkpoint: 86f118b]
- [x] Task: Add `import-linter` to `pyproject.toml` (dev dependencies). 6bfb600
- [x] Task: Create `.importlinter` configuration file. 1a071aa
- [x] Task: Define the "GUI Isolation" contract (forbid `googleapiclient` in `mygoog_gui`). 1a071aa
- [x] Task: Conductor - User Manual Verification 'Setup and Configuration' (Protocol in workflow.md) 86f118b

## Phase 2: Core Contracts [checkpoint: bb6a39c]
- [x] Task: Define the "No Reverse Dependencies" contract (lib cannot import apps). 9290dcb
- [x] Task: Define the "Core Encapsulation" contract (limit access to `mygooglib.core`). 0c51caf
- [x] Task: Run the linter and analyze existing violations (if any). 0c51caf
- [x] Task: Conductor - User Manual Verification 'Core Contracts' (Protocol in workflow.md) bb6a39c

## Phase 3: Workflow Integration
- [ ] Task: Create a simple script/command `scripts/run_arch_lint.py` (or similar) for easy execution.
- [ ] Task: Update project documentation (e.g., `conductor/workflow.md` or `README.md`) to mention this new check.
- [ ] Task: Perform a "Negative Test" (add a bad import, verify failure).
- [ ] Task: Conductor - User Manual Verification 'Workflow Integration' (Protocol in workflow.md)
