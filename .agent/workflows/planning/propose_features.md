---
description: Analyze mygooglib and propose high-value new features
---

# /propose_features

**Goal**: Prioritize next steps based on data.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve`, ensure `task.md` item "Feature Proposals" is marked `[/]` BEFORE starting.

---

1. Review Project Vision and Goals
   - Read `AUTOMATION_GOALS.md` definitions.
   - Read `docs/development/roadmap.md` status.

2. Identify TODOs
   - `Select-String -Path "mygooglib\*.py" -Pattern "TODO" -Recurse`
   - **Context**: Fixes often trump new features.

3. Analyze API Coverage
   - Read `coverage_report.md` (Output from `/coverage_audit`).
   - **Gate**:
     - **IF EXISTS**: Proceed.
     - **IF MISSING**: Run `/coverage_audit` first. Recurse.

4. Create Feature Proposal Artifact
   - **File**: `feature_proposal.md`.
   - **Template**:
     ```markdown
     # Feature Proposal: [Title]
     **Workflow Impact**: [Which W1-W6 workflow does this enhance?]
     **Value**: [Time saved, new capability]
     **Implementation**:
       - File: `mygooglib/[module].py`
       - Method: `[method_name](...)`
     ```

5. Verify Artifact
   - **Prove It**: Check file exists `feature_proposal.md`.
   - **Gate**:
     - **IF EXISTS**: Proceed.
     - **IF MISSING**: Stop. Re-create artifact. Recurse.

---

**Result**: If artifact exists, mark "Feature Proposals" as `[x]` in `task.md`.

