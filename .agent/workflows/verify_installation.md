---
description: Verify the installation and API connectivity using smoke tests
---

1. Run read-only smoke tests (safe to run anytime)
   - `python scripts/smoke_test.py all`

2. Run write tests (WARNING: This sends an email and writes to Sheets!)
   - `python scripts/smoke_test.py all --write`

3. Check specific services if needed
   - `python scripts/smoke_test.py drive-list`
   - `python scripts/smoke_test.py sheets-read --identifier "spreadsheet_id_here"`
