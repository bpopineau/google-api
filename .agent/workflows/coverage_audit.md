---
description: Compare implementation vs AUTOMATION_GOALS.md and identify gaps
---

1. Parse AUTOMATION_GOALS.md Core Actions (Section 3)
   - Read `AUTOMATION_GOALS.md` Section 3: "Core actions per service"
   - **Expected methods by service**:
     - **Drive**: upload_file, download_file, list, find_by_name, create_folder, sync_folder
     - **Sheets**: get_range, update_range, append_row
     - **Docs**: create, get_text, find_replace, append_text, export_pdf, render_template
     - **Calendar**: add_event, list_events
     - **Tasks**: list_tasklists, add_task, list_tasks, complete_task
     - **Gmail**: send_email, search_messages, mark_read

2. Scan Implemented Methods
   - `Select-String -Path "mygooglib\drive.py" -Pattern "def " | Select-Object -First 20`
   - `Select-String -Path "mygooglib\sheets.py" -Pattern "def " | Select-Object -First 20`
   - `Select-String -Path "mygooglib\gmail.py" -Pattern "def " | Select-Object -First 20`
   - `Select-String -Path "mygooglib\docs.py" -Pattern "def " | Select-Object -First 20`
   - `Select-String -Path "mygooglib\calendar.py" -Pattern "def " | Select-Object -First 20`
   - `Select-String -Path "mygooglib\tasks.py" -Pattern "def " | Select-Object -First 20`

3. Generate Coverage Report
   - **Template**:
     ```markdown
     # API Coverage Report

     ## Drive
     | Method | Status |
     |--------|--------|
     | upload_file | ✅ Implemented |
     | download_file | ✅ Implemented |
     | ... | ... |

     ## Gaps Identified
     - [List missing methods]

     ## Priority Order (from AUTOMATION_GOALS.md Section 6)
     1. [Highest priority gap]
     2. [Next priority]
     ```

4. Cross-Reference Roadmap
   - Read `docs/development/roadmap.md` Section 2 (New Feature Ideas).
   - **Check**: Are any gaps already planned?

5. Output Artifact
   - Create `coverage_report.md` with findings.
   - **Use**: This feeds into `/propose_features` for prioritization.
