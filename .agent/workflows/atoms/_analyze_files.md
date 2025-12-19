---
description: Analyze current project context and task status
---

# Atom: Analyze Files

**Role:** Systems Architect.

**Context:** This atom gathers context before any significant action. It enforces the "Thinking First" rule.

**Constraints:**
- Do NOT suggest changes during this step.
- Focus only on understanding current state.

**Task:**
1. Read `task.md` (if exists) to understand current progress.
2. Read `implementation_plan.md` (if exists) for architectural direction.
3. List files in `mygooglib/` to refresh file structure awareness.
4. Identify dependencies and relationships between modules.

**Output Format:** Markdown Summary
```markdown
## Context Analysis

### Current Task Status
- [Summary of task.md progress]

### Codebase Overview
- **Key Modules**: [list]
- **Dependencies**: [external libs]
- **Potential Impact Areas**: [files likely affected by changes]

### Recommendations
- [Any observations before proceeding]
```
