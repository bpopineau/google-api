---
description: Verify authentication token
---

# Atom: Auth Check

**Role:** Security Operations Engineer.

**Context:** This atom validates that the Google API authentication token is valid and can be refreshed.

**Constraints:**
- Do NOT proceed if authentication fails.
- Direct user to `/maintenance/setup_auth` on failure.

**Task:**
1. Run the token refresh check script.

**Execution:**
// turbo
   - `python scripts/check_token_refresh.py`

**Output Format:** JSON
```json
{
  "status": "VALID | INVALID | EXPIRED",
  "action_required": "<null | 'Run /maintenance/setup_auth'>"
}
```
