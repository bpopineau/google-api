---
description: Quick project health verification before any work
---

1. Verify Git State
// turbo
   - `git status --short`
   - **Clean**: Should show minimal or expected changes.
   - `git log -1 --oneline`
   - **Branch**: Confirm you're on the expected branch.

2. Verify Dependencies
// turbo
   - `pip install -e ".[dev,cli]"`
   - **Success**: No errors during installation.

3. Verify Core Import
// turbo
   - `python -c "from mygooglib import get_clients; print('Import OK')"`
   - **Success**: Prints "Import OK" without errors.

4. Verify Authentication
// turbo
   - `python scripts/check_token_refresh.py`
   - **Success**: Token refreshes without browser prompt.
   - **Failure**: Run `/setup_auth` to fix.

5. Quick Smoke Test
// turbo
   - `python scripts/smoke_test.py all`
   - **Tests**: Drive, Sheets, Gmail, Calendar, Tasks connectivity.
   - **Success**: All services return data without errors.

6. Verify CLI
// turbo
   - `mygoog --help`
   - **Success**: Shows available commands.

**Result**: If all steps pass, project is healthy and ready for development.
