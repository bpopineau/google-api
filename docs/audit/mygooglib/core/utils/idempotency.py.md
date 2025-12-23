# Audit Report: mygooglib/core/utils/idempotency.py

## Purpose
- Provides a local SQLite-based store to track processed items (e.g., email message IDs, file hashes) to ensure that automation scripts don't repeat the same actions if executed multiple times.

## Main Exports
- `IdempotencyStore`: Class for interacting with the local SQLite record of processed keys.
- `idempotent(...)`: Decorator that wraps functions to skip execution if a derived key has already been processed.

## Findings
- **Storage:** Currently defaults to `~/.mygooglib/idempotency.db`, which is inconsistent with the library's recent move to `~/.mygoog`. (FIXED during audit).
- **Atomicity:** `check_and_add()` uses an atomic `INSERT` to prevent race conditions in highly parallel (though unlikely for this app) environments.
- **SQLite Choice:** Appropriate for a local developer tool, avoiding external dependencies.

## TODOs
- [ ] [Consistency] Ensure all `idempotency.db` interactions use the centralized `AppConfig.config_dir` logic.
- [ ] [Feature] Add an optional `ttl` (Time To Live) for keys so they can be automatically purged or ignored after a certain duration.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
