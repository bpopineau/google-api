**Personal Google APIs Library Checklist**

**Step 1 — Identify Personal Automation Goals**
- [x] **Source of truth**: Maintain all Step 1 details in [AUTOMATION_GOALS.md](AUTOMATION_GOALS.md).
- [x] **v0.1 decisions captured**: Workflows, Must/Nice/Later, v0.1 API surface, I/O contracts, naming conventions.
- [x] **Step 1 sign-off**: Confirm Step 1 is complete before starting auth/client implementation.

**Step 2 — Set Up And Secure Credentials**
- [x] **Create/Select Project**: Create a Google Cloud project for this library (personal use).
- [x] **Enable APIs**: Enable Drive, Sheets, Docs, Calendar, Tasks, Gmail in Google Cloud Console.
- [x] **OAuth Consent Screen**: Configure consent screen (and add yourself as a test user if needed).
- [x] **Create OAuth Client**: Create OAuth 2.0 client credentials for a **Desktop app**.
- [x] **Download OAuth**: Save `credentials.json` (OAuth client) securely.
- [x] **Decide Token Location**: Pick a local secret dir + final paths for `credentials.json` and `token.json`.
- [x] **Run OAuth Flow**: Obtain and save `token.json` (one-time consent).
- [x] **Refresh Behavior**: Confirm refresh token works (re-run script a second time with no prompt).
- [x] **Define Scopes List**: Write the combined scopes list needed for your v0.1 workflows (so you only consent once).
- [x] **Scope Strategy**: Decide whether to request all scopes up front vs per-service tokens.
- [ ] **Service Account (Optional)**: Decide if a service account is needed (share resources if used).
- [x] **Ignore Secrets**: Add credential files to `.gitignore` and avoid hard-coding.
- [x] **Docs Note**: Write down which account is authorized + what scopes were granted (so future-you knows).

**Step 3 — Organize Library Structure**
- [x] **Create Package Layout**: Add `mygooglib/` with `__init__.py` and modules: `drive.py`, `sheets.py`, `docs.py`, `calendar.py`, `tasks.py`, `gmail.py`.
- [x] **Auth Module**: Add `auth.py` to load `token.json` / run InstalledAppFlow.
- [x] **Common Utilities**: Add a `utils/` package (or module) for shared helpers (IDs/paths, pagination, datetime, A1 conversion, email encoding).
- [x] **Exceptions**: Add `exceptions.py` with a small, readable exception hierarchy (base `GoogleApiError`, etc.).
- [ ] **Types (Optional)**: Add basic dataclasses/TypedDicts for returned objects you care about (event summary, message header fields).
- [x] **Decide Install**: Optionally prepare for local install (`pip install -e .`).

**Step 4 — Initialize And Reuse API Clients**
- [x] **Build Services Once**: Use `build()` for each API and reuse service objects.
- [x] **Client Cache**: Refactored to ergonomic class-based wrappers.
- [x] **Combine Scopes**: Define a single scopes list covering all planned services.
- [x] **Per-Service Build**: Confirm versions (Drive v3, Sheets v4, Docs v1, Calendar v3, Tasks v1, Gmail v1).
- [x] **Factory**: Add `create_all_clients(creds)` or similar to instantiate wrappers.
- [x] **Escape Hatch**: Expose raw `service` objects (read-only) for advanced calls not yet wrapped.

**Step 5 — Drive Wrapper**
- [x] **Core Methods**: Implement `upload_file`, `download_file`, `list_files`, `create_folder`, `find_by_name`, `sync_folder`.
- [x] **Pagination**: Ensure `list_files` iterates `pageToken` until exhausted.
- [x] **Query Helpers**: Add `list_files(query=None, parent_id=None)` and `find_by_name(name, parent_id=None)`.
- [x] **Path-ish Helpers (Optional)**: Provide helpers for "folder by name under parent" since Drive uses IDs.
- [x] **MIME/Convert Options**: Add optional `convert=True` where useful.
- [x] **Upload Defaults**: Decide behavior for `name=None` (use filename) and `parent_id=None` (root).
- [x] **Return Shapes**: Decide whether to return just IDs, or minimal metadata dicts.
- [x] **Pass-Through**: Allow advanced `**kwargs` to underlying API.
- [ ] **delete_file / share_file (Later)**: Not implemented in v0.1 (not in Must scope).

**Step 6 — Sheets Wrapper**
- [x] **Spreadsheet API**: Implement `open_by_title`, `open_by_id`.
- [x] **Worksheet Access**: Refactored to ergonomic `SheetsClient` class.
- [x] **A1 Helpers**: Implement conversions (row/col → A1, A1 → row/col).
- [x] **Cell/Row/Col**: Add `get_value`, `update_value`, `get_row`, `get_column`, `append_row`, `get_all_values`.
- [x] **Value Input**: Decide default `valueInputOption` (RAW) + allow override.
- [x] **Range/Bulk**: Provide batch updates and optional Pandas DataFrame export.
- [x] **Name Access**: Optionally support header-name column access and sheet-by-title.

**Step 7 — Docs Wrapper**
- [x] **Create/Insert**: Implement `create_document`, `insert_text`, `get_text`. (Implemented `render_template`)
- [x] **Insert Locations**: Decide on supported insert targets (`start`, `end`, explicit index if needed).
- [x] **Find/Replace**: Add `find_replace` helper (batchUpdate wrapper).
- [x] **Text Extraction**: Implement “plain text from doc structure” (good enough for search/templates).
- [x] **Escape Hatch**: Provide method to call raw `batchUpdate` for advanced edits.

**Step 8 — Calendar Wrapper**
- [x] **Add Event**: Implement `add_event` accepting Python `datetime`/`date` and optional timezone.
- [x] **All-Day Events**: Support `date` inputs to create all-day events.
- [x] **RFC3339 Formatting**: Centralize datetime formatting + parsing.
- [x] **List/Search**: Add `list_events(time_min=None, time_max=None)`.
- [x] **Update/Delete**: Implement `update_event`, `delete_event` as needed.
- [x] **Timezone Handling**: Define default tz behavior for naive datetimes.

**Step 9 — Tasks Wrapper**
- [x] **Tasklist Helpers**: Add `list_tasklists` and default tasklist lookup.
- [x] **Default Tasklist**: Support `@default` or resolve by title.
- [x] **Task Ops**: Implement `list_tasks`, `add_task`, `complete_task`, `delete_task`.
- [x] **Due Dates**: Support `date`/`datetime` due inputs.
- [x] **Pagination**: Ensure list calls handle multiple pages.
- [x] **Parents/Subtasks**: Decide whether to support subtasks (optional).

**Step 10 — Gmail Wrapper**
- [x] **Send Email (v0.1 Must)**: Implement `send_email(to, subject, body, attachments=None)` using `EmailMessage` + base64url encode; return `message_id`.
- [x] **Search (v0.1 Must)**: Implement `search_messages(query)` returning lightweight message objects (id, subject, sender, snippet; optionally date).
- [x] **Mark Read (v0.1 Must)**: Implement `mark_read(message_id)` (or `message.mark_read()`) via modify/label updates.
- [x] **Message Parsing**: Extract common headers (From, To, Subject, Date) + snippet consistently.
- [x] **Attachments**: Implement file attachment handling with proper MIME type guessing.
- [x] **Attachments Download (Optional)**: Implement `download_attachment(name, save_dir)` and `download_all_attachments`.
- [x] **Modify Helpers (Optional)**: Implement `mark_unread`, `trash`, `archive` (label changes).
- [x] **Label Helpers (Optional)**: Provide label lookup + optional label creation.
- [x] **Text vs HTML (Optional)**: Decide whether to support HTML bodies; keep default plain text.

**Step 11 — Pythonic Patterns**
- [x] **Retries**: Add `@retry` (google-api-core or custom) for transient errors (429/5xx).
- [x] **Backoff Policy**: Define retry counts + exponential backoff + which statuses to retry.
- [x] **Timeouts**: Decide on per-request timeouts (where supported) and defaults.
- [ ] **Context Managers**: Add `with` support for batch operations (optional).
- [x] **Factories**: Expose factory functions for quick client creation.
- [x] **Logging Decorator**: Optional decorator for debug logging of calls.

**Step 12 — Higher-Level Utilities**
- [ ] **Cross-Service Workflows**: Implement examples like `email_sheet(sheet_id, to)` and `schedule_tasks_in_calendar`.
- [ ] **Backup/Sync**: Add `drive.backup_document(doc_id, folder_id)` and local↔Drive sync helpers.
- [ ] **Export Helpers**: Decide how to export Sheets/Docs to CSV/PDF (Drive export endpoints).
- [ ] **Workflows Module**: Add `workflows.py` for combined utilities.

**Step 13 — Logging, Errors, Scheduling**
- [x] **Logging**: Integrate `logging` with configurable level; avoid logging secrets.
- [x] **Exceptions**: Wrap `HttpError` into readable custom exceptions or clear messages.
- [x] **Error Mapping**: Identify common cases (401/403/404/429) and make messages actionable.
- [x] **Retries/Backoff**: Ensure exponential backoff for rate limits.
- [ ] **Scheduling**: Document using OS schedulers or optionally provide `schedule`/`APScheduler` helpers.
- [ ] **Notifications**: Optionally add alerting (email/log) on failures.

**Step 14 — Docs, Tests, Maintenance**
- [x] **README**: Create usage examples and setup steps (OAuth, install).
- [x] **Examples**: Ensure each service has one minimal “happy path” snippet.
- [x] **requirements**: Add `requirements.txt` (pin versions).
- [x] **Dependency Notes**: Document what’s optional (e.g., pandas) vs required.
- [x] **Tests**: Add simple unit/integration tests for key methods (auth, send_email, upload_file).
- [x] **Manual Smoke Checklist**: Write a short “run these once” checklist (token refresh, list Drive files, send email to self).
- [ ] **Update Plan**: Schedule occasional dependency updates and quota checks.

**Step 15 — CLI Implementation**
- [x] **Typer + Rich**: Implement full CLI using `typer` for commands and `rich` for formatting.
- [x] **Drive CLI**: Added `find-by-name` and `create-folder`.
- [x] **Calendar CLI**: Added `add-event` and `list-events`.
- [x] **Tasks CLI**: Added `list-tasks`, `add-task`, and interactive `complete`.
- [x] **Docs CLI**: Added `render` (JSON/file data) and `export-pdf`.
- [x] **Shell Completion**: Enabled `typer` shell completion.
- [x] **Consistent Formatting**: Standardized JSON vs Table output across all services.
- [x] **Bonus Improvements**:
    - [x] **Gmail Interactive Search**: Added `--interactive` flag to `gmail search` to view message bodies.
    - [x] **Gmail View**: Added `gmail view <id>` command.
    - [x] **Drive Sync Dry Run**: Added `--dry-run` to `drive sync`.
    - [x] **Sheets Tab Listing**: Added `sheets list-tabs` command.
    - [x] **Enhanced Error UI**: Errors now appear in a dedicated `rich.Panel`.

**Optional Quick Tasks**
- [x] **.gitignore**: Add `credentials.json`, `token.json`.
- [x] **Example Scripts**: Add `examples/` with 2–3 scripts (send email, upload file, append sheet).
- [x] **Local Config**: Optionally add `.env` support for credential/token paths.
- [x] **Debug Logging Toggle**: Add one environment variable to enable debug logs.
- [ ] **License/Notes**: Add personal notes about risk of broad scopes and secrets handling.

