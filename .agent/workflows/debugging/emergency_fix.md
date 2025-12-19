---
description: Rapidly debug, fix, and release a critical mygooglib patch
---

1. Identify and Fix
// turbo
   - `/debug_issue`
   - **Goal**: Reproduce the bug in `scripts/repro.py` and apply minimal fix.
   - **Common locations**:
     - Auth issues: `mygooglib/auth.py`
     - API errors: `mygooglib/[service].py`
     - CLI bugs: `mygooglib/cli/[service].py`

2. Verify Fix Didn't Break Anything
// turbo
   - `/ci_local`
   - **Must pass**: Linting, unit tests, smoke tests.

3. Update Changelog
   - Add entry to `CHANGELOG.md` under new patch version:
     ```markdown
     ## 0.1.1 — YYYY-MM-DD

     ### Fixed
     - [Brief description of the fix]
     ```

4. Commit and Tag
   - `git add .`
   - `git commit -m "fix: [brief description]"`
   - `git tag v0.1.1`
   - `git push origin main --tags`

5. (Optional) Rebuild
   - `python -m build`
