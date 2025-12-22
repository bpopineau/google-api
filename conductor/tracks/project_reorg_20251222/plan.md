# Plan: Project Reorganization

Implement a modular repository structure to separate core library logic from CLI and GUI interfaces, while enabling global configuration access.

## Phase 1: Layout Scaffolding & Dependency Setup
- [ ] Task: Create new directory structure for `mygooglib`, `mygoog_cli`, and `mygoog_gui`.
- [ ] Task: Update `pyproject.toml` to define new package discovery and "extras" (`cli`, `gui`).
- [ ] Task: Implement `mg` and `mgui` entry points in `pyproject.toml`.
- [ ] Task: Conductor - User Manual Verification 'Layout Scaffolding & Dependency Setup' (Protocol in workflow.md)

## Phase 2: Core Library Reorganization
- [ ] Task: Move utility modules (`logging`, `retry`, `pagination`, etc.) to `mygooglib/core/`.
- [ ] Task: Move base components (`auth.py`, `client.py`, `config.py`, `exceptions.py`) to `mygooglib/core/`.
- [ ] Task: Move service modules (`drive.py`, `gmail.py`, `sheets.py`, etc.) to `mygooglib/services/`.
- [ ] Task: Move `workflows.py` to `mygooglib/workflows/`.
- [ ] Task: Implement standardized public API in `mygooglib/__init__.py`.
- [ ] Task: Conductor - User Manual Verification 'Core Library Reorganization' (Protocol in workflow.md)

## Phase 3: CLI & GUI Migration
- [ ] Task: Migrate existing CLI code from `mygooglib/cli/` to `mygoog_cli/` and update internal imports.
- [ ] Task: Migrate existing GUI code from `mygooglib/gui/` to `mygoog_gui/` and update internal imports.
- [ ] Task: Verify standalone installation of CLI and GUI via extras (e.g., `pip install .[cli]`).
- [ ] Task: Conductor - User Manual Verification 'CLI & GUI Migration' (Protocol in workflow.md)

## Phase 4: Configuration & Global Access
- [ ] Task: Write tests for configuration discovery in `~/.mygoog/`.
- [ ] Task: Update `mygooglib/core/config.py` to prioritize `~/.mygoog/` with fallback/migration from project root.
- [ ] Task: Verify that `mg` and `mgui` correctly locate credentials in the user home directory.
- [ ] Task: Conductor - User Manual Verification 'Configuration & Global Access' (Protocol in workflow.md)

## Phase 5: Verification & Finalization
- [ ] Task: Update all test import paths and ensure full test suite passes.
- [ ] Task: Update project documentation (`README.md`, `docs/`) to reflect the new structure.
- [ ] Task: Generate `CHANGELOG.md` migration notes for breaking changes.
- [ ] Task: Run final smoke tests across all services.
- [ ] Task: Conductor - User Manual Verification 'Verification & Finalization' (Protocol in workflow.md)
