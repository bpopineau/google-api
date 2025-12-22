---
description: Create a rigorous implementation plan with ambiguity checks
---

# /plan_feature

**Goal**: Create a blueprint so clear that execution is deterministic.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve` (Phase 2), ensure `task.md` item "Create Implementation Plan" is `[/]`.

---

1. Define the Problem & Solution
   - Create/Reset `implementation_plan.md` artifact.
   - **Header**: `# Implementation Plan - [Feature]`
   - **Section 1**: `## Problem Space`. Definition of user need.
   - **Section 2**: `## Proposed Solution`. High-level approach.

2. Define Deliverables (The Contract)
   - **Section 3**: `## Proposed Changes`
   - **Must Include**:
     - Exact file paths (e.g., `mygooglib/drive.py`).
     - Exact function signatures (inputs/outputs).
     - CLI command signatures (`mg service command --arg`).
   - **Gate**:
     - **IF VAGUE** (e.g., "Add helper"): Stop. Define signature. Recurse.
     - **IF CONCRETE** (e.g., `def get_id(url: str) -> str`): Proceed.

3. Ambiguity Check
   - Scan the plan for "magic words" that hide work:
     - "Improve", "Refactor", "Fix", "Better", "Clean up".
   - **Gate**:
     - **IF FOUND**: Stop. Replace with specific metrics/actions. Recurse.
     - **IF CLEAN**: Proceed.

4. Define Verification (The Proof)
   - **Section 4**: `## Verification Plan`
   - **Must Include**:
     - **Automated**: List of unit test case names.
     - **Manual**: Exact command to run in terminal.
     - **Success Criteria**: What output constitutes "PASS".

5. Task Extraction Strategy
   - **Section 5**: `## Task Breakdown`
   - Explicitly list the `task.md` sub-items to copy.
   - **Format**:
     ```markdown
     - [ ] Implement [Function Name]
     - [ ] Add CLI [Command Name]
     - [ ] Test [TestCase Name]
     ```

6. User Review
   - Use `notify_user` to present the plan.
   - **Gate**:
     - **IF APPROVED**: Proceed to update `task.md`.
     - **IF REJECTED**: Edit plan. Recurse.

---

**Result**: Mark `[x]` in `task.md` only after User Approval.

