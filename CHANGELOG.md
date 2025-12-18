# Changelog
 
## 0.2.0 — 2025-12-18

### Added
- **Health Improvements**: Better error hints for 403 (API Not Enabled) errors in `exceptions.py`.
- **Drive Path Resolution**: Improved `resolve_path` and CLI logic to handle human-readable paths/names automatically using name-based lookups and path traversal.
- **Sheets to Calendar Workflow**: New `mygoog workflows sheets-to-calendar` command for bulk-importing events from Google Sheets.
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
