---
description: Analyze mygooglib and propose high-value new features
---

1. Review Project Vision and Goals
   - Read `AUTOMATION_GOALS.md` — defines the 6 core workflows (W1-W6):
     - W1: Drive folder backup (`sync_folder`)
     - W2: Sheets tracker (`get_range`, `append_row`)
     - W3: Docs templating (`render_template`)
     - W4: Calendar events (`add_event`)
     - W5: Tasks capture (`add_task`)
     - W6: Gmail send (`send_email`)
   - Read `docs/development/roadmap.md` — tracks progress and future ideas.

2. Identify TODOs in the codebase
   - `Select-String -Path "mygooglib\*.py" -Pattern "TODO" -Recurse`
   - `Select-String -Path "mygooglib\cli\*.py" -Pattern "TODO" -Recurse`
   - **Look for**: Low-hanging fruit or critical fixes.

3. Analyze API coverage gaps
   - Compare implemented methods against `AUTOMATION_GOALS.md` Section 3 (Core actions).
   - **Key gaps to check**:
     - Docs: Is `render_template` fully working?
     - Drive: Is `sync_folder` recursive?
     - Sheets: Batch operations?

4. Review roadmap future ideas
   - `docs/development/roadmap.md` Section 2 lists:
     - Pandas integration
     - Batch operations
     - Google Contacts support
     - Drive path resolution

5. Create Feature Proposal Artifact
   - **File**: Create `feature_proposal.md` artifact with top 3 recommendations.
   - **Template**:
     ```markdown
     # Feature Proposal: [Title]
     **Workflow Impact**: [Which W1-W6 workflow does this enhance?]
     **Value**: [Time saved, new capability, or pain removed]
     **Effort**: [Low/Medium/High]
     **Implementation**:
       - File: `mygooglib/[module].py`
       - Method: `[method_name](...)`
       - CLI: `mygoog [command] [subcommand]`
     ```
