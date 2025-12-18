---
description: Analyze the project and propose high-value new features
---

1. Review Project Vision and Goals
   - `type AUTOMATION_GOALS.md`
   - `type docs/development/roadmap.md`
   - **Action**: Identify "Nice" or "Later" items that are not yet implemented.

2. Identify Technical Debt and TODOs
   - `grep -r "TODO" mygooglib/`
   - **Action**: Look for low-hanging fruit or critical fixes marked for later.

3. Analyze Current API Coverage
// turbo
   - `python scripts/smoke_test.py --help`
   - **Action**: Compare available CLI commands against the "Core actions" list in `AUTOMATION_GOALS.md`.

4. Create Feature Proposal Artifact
   - **Action**: Create a new artifact file `feature_proposal.md` with your top 3 recommendations.
   - **Template**:
     ```markdown
     # Feature Proposal: [Title]
     **Value**: [Why is this high value?]
     **Effort**: [Estimated complexity]
     **Implementation**: [Brief sketch]
     ```
