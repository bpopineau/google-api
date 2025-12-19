---
description: Create a git checkpoint
---

# Atom: Checkpoint

**Role:** Release Engineer.

**Context:** This atom creates a git checkpoint to save current progress.

**Constraints:**
- Prompt user for commit message if not provided.
- Use conventional commit format (e.g., `feat:`, `fix:`, `chore:`).

**Task:**
1. Stage all changes.
2. Commit with provided or generated message.

**Execution:**
   - Ask user: "Provide a commit message or press Enter for auto-generated."
   - `git add -A`
   - `git commit -m "[message]"`

**Output Format:** JSON
```json
{
  "status": "COMMITTED | NO_CHANGES",
  "commit_hash": "<short hash>",
  "message": "<commit message>"
}
```
