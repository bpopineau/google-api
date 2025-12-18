---
description: Setup Google API authentication and verify tokens
---

1. Run the interactive OAuth setup script
   - `python scripts/oauth_setup.py`

2. Verify token refresh works without user interaction
   - `python scripts/check_token_refresh.py`

3. List available files to verify Drive access (optional)
   - `python scripts/drive_list_files.py` (if configured) or run smoke test:
   - `python scripts/smoke_test.py drive-list`
