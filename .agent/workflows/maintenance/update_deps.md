---
description: Update mygooglib dependencies using uv
---

1. Update lockfile
   - `uv lock --upgrade`

2. Sync environment
   - `uv sync`

3. Verify Core Dependencies
// turbo
   - `pip show google-api-python-client google-auth google-auth-oauthlib`

4. Run Tests
// turbo
   - `pytest`
   - `python scripts/smoke_test.py all`

5. Check for Breaking Changes
   - Review changelogs for major dependencies:
     - [google-api-python-client](https://github.com/googleapis/google-api-python-client/releases)
     - [google-auth](https://github.com/googleapis/google-auth-library-python/releases)

6. (Optional) Security Audit
   - `pip install pip-audit && pip-audit`
