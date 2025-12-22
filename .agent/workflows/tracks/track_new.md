---
description: Start a new feature or bug track with spec and plan generation
---

# Workflow: /track_new [description]

> Creates a track folder with `spec.md` and `plan.md`, then registers it.

## Pre-Flight Context Load

**Required Files to Read:**
- `conductor/product.md` - Product context
- `conductor/product-guidelines.md` - UX standards
- `conductor/tech-stack.md` - Technical constraints
- `conductor/workflow.md` - Development process

---

## Step 1: Generate Track ID

**Format:** `<feature_slug>_<YYYYMMDD>`

**Examples:**
- `dark_mode_toggle_20251219`
- `fix_login_timeout_20251219`
- `sheets_batch_write_20251219`

---

## Step 2: Create Track Folder Structure

// turbo
```bash
mkdir -p .agent/workflows/tracks/<track_id>
```

---

## Step 3: Create Specification Document

**File:** `.agent/workflows/tracks/<track_id>/spec.md`

**Template:**
```markdown
# Specification: [Track Title]

## Goal
[One paragraph: What are we building and why?]

## User Story
As a [user type], I want to [action] so that [benefit].

## Acceptance Criteria
- [ ] [Criterion 1 - specific, testable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Technical Constraints
[From tech-stack.md: languages, frameworks, patterns to follow]

## Out of Scope
[Explicitly list what this track does NOT include]

## Dependencies
[Other tracks, external services, or prerequisites]
```

**Protocol:**
1. Discuss requirements with user if description is vague
2. Reference product.md for alignment with project vision
3. Reference tech-stack.md for implementation constraints

---

## Step 4: Create Implementation Plan

**File:** `.agent/workflows/tracks/<track_id>/plan.md`

**Template:**
```markdown
# Plan: [Track Title]

## Phase 1: [Phase Name]
- [ ] Task: [Description]
    - [ ] Subtask: Write unit tests
    - [ ] Subtask: Implement functionality
- [ ] Task: [Description]
- [ ] Task: Conductor - Phase Verification (Protocol in workflow.md)

## Phase 2: [Phase Name]
- [ ] Task: [Description]
- [ ] Task: Conductor - Phase Verification

## Phase 3: [Phase Name]
- [ ] Task: Final integration
- [ ] Task: Documentation updates  
- [ ] Task: Conductor - Track Completion Verification
```

**Status Markers:**
- `[ ]` - Pending
- `[~]` - In Progress
- `[x]` - Complete (append commit SHA: `[x] Task name [abc1234]`)

---

## Step 5: Create Metadata File

**File:** `.agent/workflows/tracks/<track_id>/metadata.json`

```json
{
  "id": "<track_id>",
  "title": "<Track Title>",
  "status": "pending",
  "created": "<ISO timestamp>",
  "type": "feature|bugfix",
  "checkpoints": []
}
```

---

## Step 6: Update Track Registry

**File:** `conductor/tracks.md`

**Append:**
```markdown
## [ ] Track: [Track Title]
*ID: `<track_id>`*
*Link: [spec.md](.agent/workflows/tracks/<track_id>/spec.md)*
```

---

## Step 7: User Review Gate

**CRITICAL: STOP and await explicit approval.**

Present to user:
1. Summary of the spec
2. Phase breakdown from plan
3. Estimated complexity

**Ask:** "Does this spec and plan look correct? Reply 'yes' to proceed or provide feedback."

---

## Completion

**Output:** 
- Track ID for reference
- Path to spec and plan files
- Next step: Run `/track_implement` to begin execution

