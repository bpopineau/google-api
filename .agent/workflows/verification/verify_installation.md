---
description: Verify mygooglib installation and API connectivity
---

1. Verify import works
// turbo
   - `python -c "from mygooglib import get_clients; print('Import OK')"`

2. Run read-only smoke tests (safe to run anytime)
// turbo
   - `python scripts/smoke_test.py all`
   - **Tests**: Drive list, Sheets read, Gmail search, Calendar list, Tasks list.

3. Check specific services
   - **Drive**: `python scripts/smoke_test.py drive-sync --local-path "." --drive-folder-id "<ID>" --help`
   - **Sheets**: `python scripts/smoke_test.py sheets-get --identifier "17KBIrDF3CZ0s5U8QQf0aUHmkttVbkHWt44-ApGFTvSw" --range "Sheet1!A1:C3"`
   - **Gmail**: `python scripts/smoke_test.py gmail-search --query "newer_than:7d" --max 5`

4. Run write tests (WARNING: Mutates real data!)
   - `python scripts/smoke_test.py all --write`
   - **Effects**:
     - Sends email to `brandon@esscoelectric.com`
     - Appends row to test spreadsheet
     - Creates calendar event
     - Creates task

5. Verify CLI interface
// turbo
   - `mg --help`
   - `mg drive --help`
   - `mg sheets --help`
   - `mg gmail --help`

