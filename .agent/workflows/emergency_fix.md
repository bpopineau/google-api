---
description: Rapidly debug, fix, and release a critical patch
---

1. Identify and Fix
// turbo
   - `/debug_issue`
   - **Goal**: Reproduce the bug and apply the minimal fix.

2. Verify Integrity
// turbo
   - `/ci_local`
   - **Goal**: Ensure the fix didn't break existing features (Regression Test).

3. Ship It
// turbo
   - `/release_prep`
   - **Goal**: Bump version, update changelog, and tag the release.
