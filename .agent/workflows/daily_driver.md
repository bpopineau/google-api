---
description: Initializes the workspace for a new session
---

# Workflow: /start_day

**Role:** Project Manager.

**Context:** Start of a new development session. Need to verify system health and understand current progress.

---

## Step 1: Health Check

**Task:**
- Execute: `/verification/health_check`

**Gate:**
- **IF PASS**: Proceed.
- **IF FAIL**: Stop. Address issues before continuing.

---

## Step 2: Context Load

**Role:** Systems Architect.

**Task:**
1. Execute Atom: `atoms/_analyze_files.md`
2. Read `task.md` to understand current progress.

---

## Step 3: Status Report

**Role:** Project Manager.

**Task:**
- Generate a session briefing for the user.

**Output Format:** Markdown
```markdown
## 🌅 Daily Session Report

**Current Goal:** [From task.md or "No active task"]
**System Health:** [PASS | FAIL]
**Last Activity:** [Most recent completed task]

### Recommended Next Action
- [Suggest the next slash command based on current state]
  - If task in progress: "Continue with `/lifecycle/evolve`"
  - If tests failing: "Run `/debugging/debug_issue`"
  - If clean state: "Start new work with `/planning/plan_feature`"
```

---

**Constraints:**
- Do NOT start new work automatically.
- Present options and let user decide.
