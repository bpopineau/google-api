# Specification: Task Scaffolding Scripts

## Overview
This feature introduces a suite of CLI tools to automate the creation of boilerplate code for common development tasks. By providing templates for new services and CLI commands, we ensure architectural consistency and reduce the manual effort required for both human developers and AI agents.

## Functional Requirements

### 1. Scaffolding Toolset
Implement a unified CLI tool (e.g., `mg dev scaffold`) or standalone scripts:
- **Service Scaffolding:** `python scripts/scaffold_service.py <name>`
    - Generates `mygooglib/services/<name>.py`.
    - Includes standard imports, `api_call` decorators, and type hints.
- **CLI Scaffolding:** `python scripts/scaffold_cli.py <name>`
    - Generates `mygoog_cli/<name>.py`.
    - Includes Typer app structure and standard help text.

### 2. Template Logic
- Use Python string templates or Jinja2 (if already in tech stack) for file generation.
- Templates must adhere to the project's coding standards (PEP 8, strict typing).

### 3. "Next Steps" Reporting
- Upon successful file generation, the script must print a summary to the console.
- Include the exact lines of code needed to register the new component (e.g., imports for `__init__.py`).

## Non-Functional Requirements
- **Simplicity:** Keep dependencies minimal (reuse `typer` and `rich`).
- **Safety:** Do not overwrite existing files without explicit user confirmation.

## Acceptance Criteria
- [ ] Running `python scripts/scaffold_service.py drive` generates a correctly formatted file.
- [ ] The generated code passes `ruff` linting and `mypy` type checking.
- [ ] The script correctly identifies if a file already exists and warns the user.
- [ ] "Next Steps" instructions are clear and accurate.

## Out of Scope
- Scaffolding for complex GUI components (to be considered later).
- Automatic modification of existing source files (registration is manual).
