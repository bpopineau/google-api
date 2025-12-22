# Changelog
 
## 0.6.0 — 2025-12-19

### Added
- **PySide6 GUI**: Native desktop dashboard with dark theme (`mg gui`).
- **Docs v2**: `insert_table()` and `insert_list()` for rich templates.
- **Retry Tests**: Comprehensive unit test coverage for `mygooglib/utils/retry.py` (13 tests).
- **Example Scripts**: New examples for Contacts, Sheets batch operations, and idempotent email.
- **Apps Script Bridge** (scaffolding): `mygooglib/appscript.py` module for future use.

### Changed
- Updated all documentation to reflect current feature set.

## 0.5.0 — 2025-12-19

### Added
- **Sheets Batch Context Manager**: `BatchUpdater` class for ergonomic bulk updates via `with client.batch(spreadsheet_id) as batch: ...`.
- **Gmail Attachments**: `get_attachment()` and `save_attachments()` functions for downloading attachments from search results.
- **Gmail CLI**: `mg gmail save-attachments --query "..." --dest ./folder/` command.


## 0.4.0 — 2025-12-18

### Added
- **Contacts CRUD**: `create_contact`, `update_contact`, `delete_contact` functions + CLI commands (`mg contacts add/update/delete`).
- **Sheets Batch Operations**: `batch_get` and `batch_update` for efficient multi-range operations, plus CLI (`mg sheets batch-get/batch-update`).
- **Gmail Idempotency**: `send_email` now accepts optional `idempotency_key` parameter to prevent duplicate sends using the IdempotencyStore.

## 0.3.0 — 2025-12-18

### Added
- **Pandas DataFrames for Sheets**: `to_dataframe()` and `from_dataframe()` helpers, plus `mg sheets to-df` CLI command.
- **Idempotency Store**: `mygooglib.core.utils.idempotency.IdempotencyStore` (sqlite-based) and `@idempotent` decorator to prevent duplicate script execution.
- **Contacts API**: New `ContactsClient` (People API) wrapper for listing and searching Google Contacts.

## 0.2.0 — 2025-12-18

### Added
- **Health Improvements**: Better error hints for 403 (API Not Enabled) errors in `exceptions.py`.
- **Drive Path Resolution**: Improved `resolve_path` and CLI logic to handle human-readable paths/names automatically using name-based lookups and path traversal.
- **Sheets to Calendar Workflow**: New `mg workflows sheets-to-calendar` command for bulk-importing events from Google Sheets.
- **Docs Features**: Added `find_replace` for batch text replacement in Google Docs.

### Changed
- Calendar `add_event` is now more robust, automatically parsing string inputs via `from_rfc3339`.

### Fixed
- Fixed type mismatch when handling `timedelta` in certain calendar workflows.

## 0.1.0 — 2025-12-17

### Added
- Auth + client factory: `get_creds()` and `get_clients()` (plus `create()` / `create_clients()` aliases)
- Drive helpers: `list_files`, `find_by_name`, `create_folder`, `upload_file`, `download_file`, `sync_folder` (recursive; upload/update only, no deletes)
- Sheets helpers: `get_range`, `update_range`, `append_row` with ID/title/URL resolution via Drive
- Gmail helpers: `send_email` (attachments supported), `search_messages` (lightweight dicts), `mark_read`
- Smoke test CLI: `scripts/smoke_test.py` including `all` runner (read-only by default; `--write` to enable mutations)

### Changed
- Gmail search results include `sender` while keeping `from` for backwards compatibility

### Notes
- This is a personal-use library; secrets (`credentials.json`, `token.json`) stay out of git.

