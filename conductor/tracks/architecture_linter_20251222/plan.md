# Plan: Architecture Linter

Implementation of automated architectural constraints using `import-linter`.

## Phase 1: Setup and Configuration
- [ ] Task: Add `import-linter` to `pyproject.toml` (dev dependencies).
- [ ] Task: Create `.importlinter` configuration file.
- [ ] Task: Define the "GUI Isolation" contract (forbid `googleapiclient` in `mygoog_gui`).
- [ ] Task: Conductor - User Manual Verification 'Setup and Configuration' (Protocol in workflow.md)

## Phase 2: Core Contracts
- [ ] Task: Define the "No Reverse Dependencies" contract (lib cannot import apps).
- [ ] Task: Define the "Core Encapsulation" contract (limit access to `mygooglib.core`).
- [ ] Task: Run the linter and analyze existing violations (if any).
- [ ] Task: Conductor - User Manual Verification 'Core Contracts' (Protocol in workflow.md)

## Phase 3: Workflow Integration
- [ ] Task: Create a simple script/command `scripts/run_arch_lint.py` (or similar) for easy execution.
- [ ] Task: Update project documentation (e.g., `conductor/workflow.md` or `README.md`) to mention this new check.
- [ ] Task: Perform a "Negative Test" (add a bad import, verify failure).
- [ ] Task: Conductor - User Manual Verification 'Workflow Integration' (Protocol in workflow.md)
