---
description: Execute the current track's plan with TDD and phase checkpoints
---

# Workflow: /track_implement

> Executes tasks from the active track's `plan.md` following TDD workflow.

## Pre-Flight

1. **Find Active Track:**
   - Read `conductor/tracks.md`
   - Find track marked `[~]` (in-progress)
   - If none, find first `[ ]` (pending) and activate it

2. **Load Context:**
   - Read `.agent/workflows/tracks/<track_id>/spec.md`
   - Read `.agent/workflows/tracks/<track_id>/plan.md`
   - Read `conductor/workflow.md` for process rules
   - Read `conductor/tech-stack.md` for constraints

---

## Task Execution Loop

**For each unchecked task `[ ]` in plan.md:**

### Step 1: Mark In Progress
- Update plan.md: Change `[ ]` to `[~]`

### Step 2: TDD Red Phase (Write Failing Tests)
1. Create test file for the feature
2. Write tests that define expected behavior
3. Run tests and **confirm they FAIL**
   ```bash
   # Example
   uv run pytest tests/test_<feature>.py -v
   ```

### Step 3: TDD Green Phase (Implement)
1. Write minimum code to make tests pass
2. Run tests and **confirm they PASS**
3. Check coverage:
   ```bash
   uv run pytest --cov=mygooglib tests/test_<feature>.py
   ```

### Step 4: Refactor (Optional)
- Improve code clarity with tests as safety net
- Re-run tests to confirm no regressions

### Step 5: Quality Gates
Before marking complete, verify:
- [ ] All tests pass
- [ ] Coverage >= 80% for new code
- [ ] Code follows style guide (run `uv run ruff check . --fix`)
- [ ] Type hints added (`uv run mypy mygooglib/`)
- [ ] No linting errors

### Step 6: Commit Changes
```bash
git add .
git commit -m "<type>(<scope>): <description>"
```

**Commit Types:** `feat`, `fix`, `test`, `refactor`, `docs`, `chore`

### Step 7: Attach Git Note
```bash
# Get commit hash
COMMIT=$(git log -1 --format="%H")

# Create detailed note
git notes add -m "Task: <task description>
Files: <list of changed files>
Summary: <what was done and why>" $COMMIT
```

### Step 8: Mark Complete
- Update plan.md: Change `[~]` to `[x]`
- Append first 7 chars of commit SHA: `[x] Task name [abc1234]`
- Commit plan update:
  ```bash
  git add .agent/workflows/tracks/<track_id>/plan.md
  git commit -m "conductor(plan): Mark task complete"
  ```

---

## Phase Completion Protocol

**Trigger:** When completing last task of a phase.

### Step 1: Announce Phase Complete
Inform user: "Phase [N] complete. Beginning verification protocol."

### Step 2: Full Test Suite
```bash
CI=true uv run pytest
```
- If fails: Debug up to 2 attempts, then ask user for help

### Step 3: Manual Verification Plan
Present step-by-step verification appropriate to the change:

**Frontend Example:**
```
1. Start server: `uv run mygoog`
2. Navigate to: [affected page]
3. Verify: [specific behavior]
```

**Backend Example:**
```
1. Run command: `uv run mygoog <command>`
2. Expected output: [description]
```

### Step 4: Await User Confirmation
**CRITICAL:** Ask user: "Does this meet your expectations? Reply 'yes' or provide feedback."

**PAUSE** - Do not continue without explicit confirmation.

### Step 5: Create Checkpoint Commit
```bash
git add .
git commit -m "conductor(checkpoint): Phase N complete"
CHECKPOINT=$(git log -1 --format="%H")
```

### Step 6: Attach Verification Report
```bash
git notes add -m "Phase Checkpoint: [Phase Name]

Automated Tests: PASSED
Manual Verification: [user's confirmation]

Steps Verified:
- [step 1]
- [step 2]

User Confirmation: Yes" $CHECKPOINT
```

### Step 7: Update Plan with Checkpoint
- Add checkpoint SHA to phase heading: `## Phase N: [Name] [checkpoint: abc1234]`
- Commit: `conductor(plan): Mark Phase N complete`

---

## Track Completion

When all phases are complete:

1. Update `conductor/tracks.md`: Change `[~]` to `[x]`
2. Update `metadata.json`: Set status to `complete`
3. Final commit: `conductor(track): Complete <track_id>`

**Output:** Summary of all completed tasks, tests passed, and files changed.
