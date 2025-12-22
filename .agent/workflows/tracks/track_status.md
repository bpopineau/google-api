---
description: Display status of all project tracks and current progress
---

# Workflow: /track_status

> Quick overview of all tracks and the active track's progress.

## Step 1: Read Track Registry

**File:** `conductor/tracks.md`

Parse and display all tracks with status:
- `[ ]` - Pending (not started)
- `[~]` - Active (in progress)
- `[x]` - Complete

---

## Step 2: Summarize Active Track

If an active track `[~]` exists:

1. Read `.agent/workflows/tracks/<track_id>/plan.md`
2. Calculate progress:
   - Count total tasks
   - Count completed `[x]` tasks
   - Show percentage
3. Display current phase and next uncompleted task

---

## Step 3: Output Format

```
# Track Status Report

## Active Track: [Track Title]
- **ID:** <track_id>
- **Progress:** 5/12 tasks (42%)
- **Current Phase:** Phase 2 - GUI Implementation
- **Next Task:** Create ActivityWidget

## All Tracks

| Status | Track | Created |
|--------|-------|---------|
| [~] | Implement Local File Sync | 2025-12-19 |
| [ ] | Add Settings Page | 2025-12-18 |
| [x] | Fix Login Bug | 2025-12-15 |
```

---

## Optional: Detailed View

If user asks for details on a specific track:
- Show full plan.md contents
- List all checkpoints with commit SHAs
- Show spec.md acceptance criteria status

