---
description: Run smoke tests against live API (Read-only)
---

# Atom: Smoke Test

**Role:** Integration Test Engineer.

**Context:** This atom runs end-to-end smoke tests against the live Google APIs to verify real-world functionality.

**Constraints:**
- Read-only operations only.
- Stop on any API failure.

**Task:**
1. Run the smoke test script for all services.

**Execution:**
// turbo
   - `python scripts/smoke_test.py all`

**Output Format:** JSON
```json
{
  "status": "PASS | FAIL",
  "services_tested": ["drive", "sheets", "gmail", "calendar", "tasks", "docs"],
  "failures": ["<list of failed services>"]
}
```

