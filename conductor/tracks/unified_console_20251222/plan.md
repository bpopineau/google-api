# Plan: Unified Debug Console (REPL)

Implementation of an interactive IPython-based console with pre-loaded context.

## Phase 1: Environment and Core Logic [checkpoint: 4bf0a0c]
- [x] Task: Add `ipython` to `pyproject.toml` (dev dependencies). 3b43f69
- [x] Task: Create `mygoog_cli/console.py` to house the REPL initialization logic. 5c2bda8
- [x] Task: Implement the "Context Builder" that authenticates and imports all required objects. 5c2bda8
- [x] Task: Conductor - User Manual Verification 'Environment and Core Logic' (Protocol in workflow.md) 4bf0a0c
- [ ] Task: Conductor - User Manual Verification 'Environment and Core Logic' (Protocol in workflow.md)

## Phase 2: CLI Integration
- [x] Task: Add the `console` command to `mygoog_cli/main.py` (or the relevant entry point). 292c41f
- [x] Task: Ensure the console correctly handles authentication errors (redirecting to oauth if needed). 292c41f
- [x] Task: Add a "Help" banner that prints on startup, listing the available pre-loaded objects. 292c41f
- [x] Task: Conductor - User Manual Verification 'CLI Integration' (Protocol in workflow.md)

## Phase 3: Verification and UX
- [ ] Task: Verify tab-completion works for nested Google API calls.
- [ ] Task: Ensure the console respects the current project configuration (e.g., custom scopes).
- [ ] Task: Perform a "Smoke Test" by running a few common commands in the console.
- [ ] Task: Conductor - User Manual Verification 'Verification and UX' (Protocol in workflow.md)
