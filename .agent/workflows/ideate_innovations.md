---
description: Generate and propose creative, outside-the-box feature ideas
---

1. Explore Possibilities
   - Review the list of available Google APIs (Drive, Sheets, Gmail, Calendar, Tasks).
   - **Thought Experiment**: "If I had a magic wand and these APIs, what would be the coolest thing I could automate?"
   - **Focus**: Look for cross-service synergies (e.g., "Email to Sheet to Calendar"), "Delighters" (unexpected conveniences), or AI augmentations (if applicable).

2. Generate Ideas
   - List at least 5 "wild" ideas. Do not filter for feasibility yet.
   - Example Stimuli:
     - "How can we visualize Drive usage in Sheets?"
     - "Can we make a 'Morning Briefing' Doc generated from Calendar and Tasks?"
     - "Can I email a command to my system to trigger a backup?"

3. Refine and Select
   - Pick the top 3 ideas that are:
     - **Novel**: Not just a standard CRUD operation.
     - **Valuable**: Solves a real (or unarticulated) problem.
     - **Feasible**: Possible with the current authentication scopes (or minor additions).

4. Create Proposal Artifact
   - **Action**: Create a new artifact file `creative_proposals.md` for User Review.
   - **Template**:
     ```markdown
     # Creative Proposal: [Name]
     **The Spark**: [What inspired this?]
     **The Magic**: [What does the user experience?]
     **How it Works**: [High-level technical sketch]
     **Why it's "Outside the Box"**: [Differentiation]
     ```

5. Request Approval
   - Use `notify_user` to present `creative_proposals.md`.
   - **Constraint**: Do NOT start implementation until specifically approved.
