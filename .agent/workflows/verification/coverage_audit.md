---
description: Compare implementation vs AUTOMATION_GOALS.md and identify gaps
---

# /coverage_audit

**Goal**: Identify what is built vs what is needed.

## ⚠️ Task Management
- **Rule**: If run as part of `/evolve`, ensure `task.md` item "Coverage Audit" is marked `[/]` BEFORE starting.

---

1. Parse AUTOMATION_GOALS.md Core Actions (Section 3)
   - Read `AUTOMATION_GOALS.md` Section 3: "Core actions per service"
   - **Context**: Know what strict success looks like (specific method names).

2. Scan Implemented Methods
   - `Select-String -Path "mygooglib\*.py" -Pattern "def " | Select-Object -First 50`
   - **Gate**:
     - **IF METHODS FOUND**: Proceed.
     - **IF EMPTY**: Stop. Verify path. Recurse.

3. Generate Coverage Report
   - Create `coverage_report.md` using the template below.
   - **Template**:
     ```markdown
     # API Coverage Report

     ## Drive
     | Method | Status |
     |--------|--------|
     | upload_file | ✅ Implemented |
     | download_file | ✅ Implemented |

     ## Gap Analysis
     - [List missing methods]

     ## Optimization Opportunities
     - [List potential improvements]
     ```

4. Cross-Reference Roadmap
   - Read `docs/development/roadmap.md`.
   - **Check**: Are any gaps already planned?

5. Verify Artifact
   - **Prove It**: Check file exists `coverage_report.md`.
   - **Gate**:
     - **IF EXISTS**: Proceed.
     - **IF MISSING**: Stop. Re-create artifact. Recurse.

---

**Result**: If artifact exists, mark "Coverage Audit" as `[x]` in `task.md`.

