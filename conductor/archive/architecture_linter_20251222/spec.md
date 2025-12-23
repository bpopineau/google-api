# Specification: Architecture Linter

## Overview
This feature introduces automated architectural enforcement to ensure that the project maintains its layered structure. By using `import-linter`, we will define strict contracts (e.g., "The GUI cannot import raw Google API clients") that prevent code drift and ensure that components remain decoupled and maintainable.

## Functional Requirements

### 1. Tool Selection
- Integrate `import-linter` into the project's development dependencies.
- Define a `.importlinter` configuration file in the project root.

### 2. Architectural Contracts
Implement the following contracts:
- **GUI Isolation:** `mygoog_gui` modules are forbidden from importing `googleapiclient` or `google.auth`. They must use `mygooglib`.
- **Core Encapsulation:** `mygoog_cli` and `mygoog_gui` should avoid importing directly from `mygooglib.core` (whenever possible), preferring the public `mygooglib.services`.
- **No Reverse Dependencies:** Library modules (`mygooglib`) cannot import from application modules (`mygoog_cli`, `mygoog_gui`).

### 3. Integration
- Create a developer-friendly command (e.g., `python -m lint_arch` or a `scripts/` wrapper).
- Ensure the linter can be run in CI (exit code 1 on failure).

## Non-Functional Requirements
- **Performance:** Architectural linting should be fast (< 2 seconds).
- **Clear Feedback:** When a contract is violated, the linter must clearly identify the illegal import and the file where it occurs.

## Acceptance Criteria
- [ ] `import-linter` is added to `pyproject.toml`.
- [ ] A `.importlinter` file exists with defined contracts.
- [ ] Running the linter on the current codebase passes (or identifies existing violations to be fixed).
- [ ] Intentionally adding a forbidden import (e.g., `import googleapiclient` in a GUI file) causes the linter to fail.

## Out of Scope
- Automated code fixing/refactoring (manual fixing only).
- Performance linting or standard code style linting (handled by Ruff).
