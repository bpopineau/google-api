---
description: Run unit tests with pytest and return structured results
---

# Atom: Run Tests

**Role:** QA Automation Engineer.

**Context:** This atom runs the project's unit test suite to verify code correctness.

**Constraints:**
- Do NOT proceed past this atom if tests fail.
- If tests fail, output the failure log and stop.

**Task:**
1. Execute the test suite using `pytest -v`.

**Execution:**
// turbo
   - `pytest -v`

**Output Format:** JSON
```json
{
  "status": "PASS | FAIL",
  "passed_count": "<integer>",
  "failed_count": "<integer>",
  "critical_failures": ["<list of failed test names>"]
}
```

