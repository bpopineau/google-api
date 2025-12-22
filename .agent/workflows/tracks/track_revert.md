---
description: Revert a track, phase, or task using git history and notes
---

# Workflow: /track_revert [target]

> Smart revert that understands logical units of work.

## Target Options

- `/track_revert task` - Revert the last completed task
- `/track_revert phase` - Revert the current/last phase
- `/track_revert track` - Revert entire track
- `/track_revert <commit_sha>` - Revert to specific checkpoint

---

## Step 1: Analyze Git History

1. Find relevant commits using git notes:
   ```bash
   git log --oneline --notes
   ```

2. Identify commits belonging to the track/phase/task

---

## Step 2: Confirm Revert Scope

**CRITICAL:** Present to user:
- List of commits to be reverted
- Files that will be affected
- Any data that might be lost

**Ask:** "This will revert [N] commits affecting [files]. Continue? (yes/no)"

**PAUSE** - Await explicit confirmation.

---

## Step 3: Execute Revert

### Option A: Soft Revert (Recommended)
Keeps history, creates new commit undoing changes:
```bash
git revert --no-commit <oldest_sha>..<newest_sha>
git commit -m "revert(track): Revert <description>"
```

### Option B: Hard Reset (Destructive)
Only if user explicitly requests and understands consequences:
```bash
git reset --hard <checkpoint_sha>
```

---

## Step 4: Update Plan Status

1. Read `.agent/workflows/tracks/<track_id>/plan.md`
2. Change reverted tasks from `[x]` back to `[ ]`
3. Remove commit SHAs from reverted tasks
4. Remove checkpoint markers if reverting phases

---

## Step 5: Update Track Registry

If reverting entire track:
1. Update `conductor/tracks.md`: Change `[x]` or `[~]` back to `[ ]`
2. Update `metadata.json`: Reset status to `pending`

---

## Step 6: Create Revert Note

```bash
REVERT_SHA=$(git log -1 --format="%H")
git notes add -m "REVERT: <target>

Scope: [task|phase|track]
Reverted commits: <list>
Reason: <user-provided reason>
Original checkpoint: <sha>" $REVERT_SHA
```

---

## Completion

**Output:**
- Confirm what was reverted
- Show current state of plan.md
- Provide next steps (e.g., "Run /track_implement to restart")

