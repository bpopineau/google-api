---
description: Generate creative, outside-the-box feature ideas for mygooglib
---

1. Review Current Capabilities
   - **Services**: Drive, Sheets, Gmail, Docs, Calendar, Tasks.
   - **Key workflows from AUTOMATION_GOALS.md**:
     - W1: Drive sync (`sync_folder`)
     - W2: Sheets tracker (`get_range`, `append_row`)
     - W3: Docs templating (`render_template`)
     - W4: Calendar events (`add_event`)
     - W5: Tasks capture (`add_task`)
     - W6: Gmail send (`send_email`)

2. Thought Experiments
   - **Cross-service synergies**:
     - "Sheets → Calendar": Auto-create events from a spreadsheet schedule.
     - "Gmail → Sheets": Log incoming emails to a tracking spreadsheet.
     - "Tasks → Docs": Generate a weekly task summary document.
     - "Calendar → Gmail": Email daily agenda each morning.
   - **Delighters**:
     - "Morning Briefing Doc" generated from Calendar + Tasks + Weather API.
     - "Email a command" to trigger backups or reports.
     - "Natural language date parsing" for task due dates.
   - **AI augmentation**:
     - Summarize email threads before logging to Sheets.
     - Auto-categorize uploaded Drive files.

3. Generate 5+ Wild Ideas
   - List ideas without filtering for feasibility.
   - Push beyond "just another CRUD wrapper."

4. Refine Top 3 Ideas
   - **Criteria**:
     - Novel: Not just another API wrapper method.
     - Valuable: Saves time or enables new workflows.
     - Feasible: Possible with current OAuth scopes.

5. Create Proposal Artifact
   - **File**: `creative_proposals.md`
   - **Template**:
     ```markdown
     # Creative Proposal: [Name]

     **The Spark**: [What inspired this?]
     **The Magic**: [What does the user experience?]
     **How it Works**:
       - Services: [Drive, Sheets, Gmail, etc.]
       - New methods: `mygooglib.[service].[method]()`
       - CLI: `mg [command]`
     **Why it's "Outside the Box"**: [What makes this special?]
     ```

6. Request Approval
   - Use `notify_user` to present `creative_proposals.md`.
   - **Constraint**: Do NOT implement until explicitly approved.

