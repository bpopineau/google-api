---
description: Perform a full clean, upgrade, and verification cycle
---

1. Update Dependencies
// turbo
   - `/update_deps`
   - **Goal**: Get the latest libraries.

2. Deep Clean
// turbo
   - `/clean_reset`
   - **Goal**: Ensure no stale artifacts interfere with the upgrade.

3. Verify Everything
// turbo
   - `/ci_local`
   - **Goal**: Run the full suite (Auth check + Unit tests + Integration writes).

4. Synchronize Documentation
// turbo
   - `/update_docs`
   - **Goal**: Ensure docs match the upgraded environment.
