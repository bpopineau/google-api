# Changelog

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
