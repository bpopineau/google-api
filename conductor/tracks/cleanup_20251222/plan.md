# Track Plan: Repo Cleanup

## Phase 1: Deletion and Core Verification
This phase focuses on removing the unused files and ensuring the core application remains functional.

- [x] Task: Remove Unused Files and Directories [5a107bc]
    - [x] Sub-task: Delete `.streamlit/` directory
    - [x] Sub-task: Delete `mygooglib/cli/` directory
    - [x] Sub-task: Delete `mygooglib/gui/` directory
    - [x] Sub-task: Delete `test_temp.md` file
    - [x] Sub-task: Delete `pytest_output.txt` file

- [x] Task: Verify Core Functionality
    - [x] Sub-task: Run standard test suite (`pytest`)
    - [x] Sub-task: Verify CLI help command (`mg --help`)
    - [x] Sub-task: Verify GUI package import (`python -c "import mygoog_gui.main"`)

- [x] Task: Conductor - User Manual Verification 'Deletion and Core Verification' [a81207c]

## Phase 1: Deletion and Core Verification [checkpoint: a81207c]

## Phase 2: Static Analysis and Cleanup
This phase ensures that no broken imports or type issues were introduced.

- [x] Task: Run Linting Checks
    - [x] Sub-task: Run `ruff check .` and fix any issues
    - [x] Sub-task: Run `ruff format .`

- [x] Task: Run Type Checks
    - [x] Sub-task: Run `mypy .` and resolve any type errors resulting from the deletions

- [ ] Task: Conductor - User Manual Verification 'Static Analysis and Cleanup' (Protocol in workflow.md)
