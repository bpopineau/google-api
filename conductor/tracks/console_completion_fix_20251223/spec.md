# Specification: Console Tab Completion Fix for Nested Calls

## Goal
Investigate and resolve the environment-specific tab completion issue for nested calls in the IPython console. Currently, while the console is structurally sound, `drive.files.` + Tab does not consistently populate methods in all terminal environments (e.g., PowerShell, CMD, Windows Terminal, VS Code integrated terminal).

## User Story
As a developer using `mg console`, I want tab completion to consistently work for nested API calls like `drive.files.<Tab>` across all terminal environments so that I can efficiently explore and use the Google API without needing to reference documentation.

## Acceptance Criteria
- [ ] Identified root cause of inconsistent tab completion behavior across environments.
- [ ] `drive.files.<Tab>` populates available methods (`list`, `create`, `get`, etc.) in PowerShell.
- [ ] `drive.files.<Tab>` populates available methods in Windows CMD.
- [ ] `drive.files.<Tab>` populates available methods in VS Code integrated terminal.
- [ ] Existing `test_console_completions.py` tests continue to pass.
- [ ] Document any terminal-specific requirements or limitations.

## Technical Constraints
From `tech-stack.md`:
- **Interactive Debugging:** IPython
- **CLI:** Typer + Rich
- Use `uv` for package management.
- Adhere to existing code patterns in `mygoog_cli/console.py`.

## Out of Scope
- Changes to the core Google API client library behavior.
- Support for non-Windows environments (may work by default, but not primary focus).
- GUI-based REPL or console.

## Dependencies
- Completed Track: Unified Debug Console (`unified_console_20251222`) - provides the base implementation.
- IPython's completion system behavior.
