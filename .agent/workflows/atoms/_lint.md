---
description: Run linter and formatter
---

# Atom: Lint

**Role:** Code Quality Enforcer.

**Context:** This atom ensures code adheres to project style standards using Ruff.

**Constraints:**
- Fix auto-fixable issues automatically.
- Stop and report if unfixable errors remain.

**Task:**
1. Format all Python files.
2. Run linter with auto-fix enabled.

**Execution:**
// turbo
   - `ruff format .`
// turbo
   - `ruff check . --fix`

**Output Format:** JSON
```json
{
  "status": "CLEAN | ERROR",
  "errors_fixed": "<integer>",
  "remaining_errors": ["<list of unfixed issues>"]
}
```
