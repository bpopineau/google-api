---
description: Setup mygooglib OAuth authentication and verify token refresh
---

1. Ensure credentials.json exists
   - **Check**: Verify `credentials.json` is in the project root (from Google Cloud Console).
   - **Docs**: See `docs/guides/configuration.md` for Google Cloud setup instructions.

2. Run the interactive OAuth setup script
   - `python scripts/oauth_setup.py`
   - **Result**: This creates `token.json` with your refresh token.

3. Verify token refresh works without user interaction
   - `python scripts/check_token_refresh.py`
   - **Success**: Should print "Token refreshed successfully" without opening a browser.

4. Quick connectivity check
// turbo
   - `python scripts/smoke_test.py all`
   - **Verifies**: Drive (list), Sheets (read), Gmail (search), Calendar (list), Tasks (list).

5. Full write verification (optional, mutates real data)
   - `python scripts/smoke_test.py all --write`
   - **Warning**: This sends a test email and writes to your test spreadsheet.

