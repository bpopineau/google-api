---
description: Install project dependencies safely
---

# Atom: Install Dependencies

**Role:** Build Engineer.

**Context:** This atom installs the project's dependencies in editable mode.

**Constraints:**
- Stop on network or PyPI failures.
- Install dev and CLI extras.

**Task:**
1. Install the package with all development dependencies.

**Execution:**
// turbo
   - `pip install -e ".[dev,cli]"`

**Output Format:** JSON
```json
{
  "status": "SUCCESS | FAIL",
  "packages_installed": "<integer>",
  "error": "<null | error message>"
}
```
