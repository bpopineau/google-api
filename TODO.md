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
- [ ] **Decide Token Location**: Pick a local secret dir + final paths for `credentials.json` and `token.json`.
- [ ] **Run OAuth Flow**: Obtain and save `token.json` (one-time consent).
- [ ] **Refresh Behavior**: Confirm refresh token works (re-run script a second time with no prompt).
- [ ] **Define Scopes List**: Write the combined scopes list needed for your v0.1 workflows (so you only consent once).
- [ ] **Scope Strategy**: Decide whether to request all scopes up front vs per-service tokens.
- [ ] **Service Account (Optional)**: Decide if a service account is needed (share resources if used).
- [ ] **Ignore Secrets**: Add credential files to `.gitignore` and avoid hard-coding.
- [ ] **Docs Note**: Write down which account is authorized + what scopes were granted (so future-you knows).

**Step 3 — Organize Library Structure**
- [ ] **Create Package Layout**: Add `mygooglib/` with `__init__.py` and modules: `drive.py`, `sheets.py`, `docs.py`, `calendar.py`, `tasks.py`, `gmail.py`.
- [ ] **Auth Module**: Add `auth.py` to load `token.json` / run InstalledAppFlow.
- [ ] **Common Utilities**: Add a `utils/` package (or module) for shared helpers (IDs/paths, pagination, datetime, A1 conversion, email encoding).
- [ ] **Exceptions**: Add `exceptions.py` with a small, readable exception hierarchy (base `GoogleApiError`, etc.).
- [ ] **Types (Optional)**: Add basic dataclasses/TypedDicts for returned objects you care about (event summary, message header fields).
- [ ] **Decide Install**: Optionally prepare for local install (`pip install -e .`).

**Step 4 — Initialize And Reuse API Clients**
- [ ] **Build Services Once**: Use `build()` for each API and reuse service objects.
- [ ] **Client Cache**: Decide if you want a simple singleton cache keyed by (service, version, user) to avoid rebuilding.
- [ ] **Combine Scopes**: Define a single scopes list covering all planned services.
- [ ] **Per-Service Build**: Confirm versions (Drive v3, Sheets v4, Docs v1, Calendar v3, Tasks v1, Gmail v1).
- [ ] **Factory**: Add `create_all_clients(creds)` or similar to instantiate wrappers.
- [ ] **Escape Hatch**: Expose raw `service` objects (read-only) for advanced calls not yet wrapped.

**Step 5 — Drive Wrapper**
- [ ] **Core Methods**: Implement `upload_file`, `download_file`, `list_files`, `create_folder`, `delete_file`, `share_file`.
- [ ] **Pagination**: Ensure `list_files` iterates `pageToken` until exhausted.
- [ ] **Query Helpers**: Add `list_files(query=None, parent_id=None)` and `find_file(name, parent_id=None)`.
- [ ] **Path-ish Helpers (Optional)**: Provide helpers for “folder by name under parent” since Drive uses IDs.
- [ ] **MIME/Convert Options**: Add optional `convert=True` where useful.
- [ ] **Upload Defaults**: Decide behavior for `name=None` (use filename) and `parent_id=None` (root).
- [ ] **Return Shapes**: Decide whether to return just IDs, or minimal metadata dicts.
- [ ] **Pass-Through**: Allow advanced `**kwargs` to underlying API.

**Step 6 — Sheets Wrapper**
- [ ] **Spreadsheet API**: Implement `open_by_title`, `open_by_id`.
- [ ] **Worksheet Access**: Decide on worksheet object model (spreadsheet object + worksheet objects vs simple methods).
- [ ] **A1 Helpers**: Implement conversions (row/col → A1, A1 → row/col).
- [ ] **Cell/Row/Col**: Add `get_value`, `update_value`, `get_row`, `get_column`, `append_row`, `get_all_values`.
- [ ] **Value Input**: Decide default `valueInputOption` (RAW) + allow override.
- [ ] **Range/Bulk**: Provide batch updates and optional Pandas DataFrame export.
- [ ] **Name Access**: Optionally support header-name column access and sheet-by-title.
- [ ] **Slicing (Later)**: Optionally support slice-based range reads/updates.

**Step 7 — Docs Wrapper**
- [ ] **Create/Insert**: Implement `create_document`, `insert_text`, `get_text`.
- [ ] **Insert Locations**: Decide on supported insert targets (`start`, `end`, explicit index if needed).
- [ ] **Find/Replace**: Add `find_replace` helper (batchUpdate wrapper).
- [ ] **Text Extraction**: Implement “plain text from doc structure” (good enough for search/templates).
- [ ] **Escape Hatch**: Provide method to call raw `batchUpdate` for advanced edits.

**Step 8 — Calendar Wrapper**
- [ ] **Add Event**: Implement `add_event` accepting Python `datetime`/`date` and optional timezone.
- [ ] **All-Day Events**: Support `date` inputs to create all-day events.
- [ ] **RFC3339 Formatting**: Centralize datetime formatting + parsing.
- [ ] **List/Search**: Add `list_events(time_min=None, time_max=None)`.
- [ ] **Update/Delete**: Implement `update_event`, `delete_event` as needed.
- [ ] **Timezone Handling**: Define default tz behavior for naive datetimes.

**Step 9 — Tasks Wrapper**
- [ ] **Tasklist Helpers**: Add `list_tasklists` and default tasklist lookup.
- [ ] **Default Tasklist**: Support `@default` or resolve by title.
- [ ] **Task Ops**: Implement `list_tasks`, `add_task`, `complete_task`, `delete_task`.
- [ ] **Due Dates**: Support `date`/`datetime` due inputs.
- [ ] **Pagination**: Ensure list calls handle multiple pages.
- [ ] **Parents/Subtasks**: Decide whether to support subtasks (optional).

**Step 10 — Gmail Wrapper**
- [ ] **Send Email (v0.1 Must)**: Implement `send_email(to, subject, body, attachments=None)` using `EmailMessage` + base64url encode; return `message_id`.
- [ ] **Search (v0.1 Must)**: Implement `search_messages(query)` returning lightweight message objects (id, subject, sender, snippet; optionally date).
- [ ] **Mark Read (v0.1 Must)**: Implement `mark_read(message_id)` (or `message.mark_read()`) via modify/label updates.
- [ ] **Message Parsing**: Extract common headers (From, To, Subject, Date) + snippet consistently.
- [ ] **Attachments**: Implement file attachment handling with proper MIME type guessing.
- [ ] **Attachments Download (Optional)**: Implement `download_attachment(name, save_dir)` and `download_all_attachments`.
- [ ] **Modify Helpers (Optional)**: Implement `mark_unread`, `trash`, `archive` (label changes).
- [ ] **Label Helpers (Optional)**: Provide label lookup + optional label creation.
- [ ] **Text vs HTML (Optional)**: Decide whether to support HTML bodies; keep default plain text.

**Step 11 — Pythonic Patterns**
- [ ] **Retries**: Add `@retry` (google-api-core or custom) for transient errors (429/5xx).
- [ ] **Backoff Policy**: Define retry counts + exponential backoff + which statuses to retry.
- [ ] **Timeouts**: Decide on per-request timeouts (where supported) and defaults.
- [ ] **Context Managers**: Add `with` support for batch operations (optional).
- [ ] **Factories**: Expose factory functions for quick client creation.
- [ ] **Logging Decorator**: Optional decorator for debug logging of calls.

**Step 12 — Higher-Level Utilities**
- [ ] **Cross-Service Workflows**: Implement examples like `email_sheet(sheet_id, to)` and `schedule_tasks_in_calendar`.
- [ ] **Backup/Sync**: Add `drive.backup_document(doc_id, folder_id)` and local↔Drive sync helpers.
- [ ] **Export Helpers**: Decide how to export Sheets/Docs to CSV/PDF (Drive export endpoints).
- [ ] **Workflows Module**: Add `workflows.py` for combined utilities.

**Step 13 — Logging, Errors, Scheduling**
- [ ] **Logging**: Integrate `logging` with configurable level; avoid logging secrets.
- [ ] **Exceptions**: Wrap `HttpError` into readable custom exceptions or clear messages.
- [ ] **Error Mapping**: Identify common cases (401/403/404/429) and make messages actionable.
- [ ] **Retries/Backoff**: Ensure exponential backoff for rate limits.
- [ ] **Scheduling**: Document using OS schedulers or optionally provide `schedule`/`APScheduler` helpers.
- [ ] **Notifications**: Optionally add alerting (email/log) on failures.

**Step 14 — Docs, Tests, Maintenance**
- [ ] **README**: Create usage examples and setup steps (OAuth, install).
- [ ] **Examples**: Ensure each service has one minimal “happy path” snippet.
- [ ] **requirements**: Add `requirements.txt` (pin versions).
- [ ] **Dependency Notes**: Document what’s optional (e.g., pandas) vs required.
- [ ] **Tests**: Add simple unit/integration tests for key methods (auth, send_email, upload_file).
- [ ] **Manual Smoke Checklist**: Write a short “run these once” checklist (token refresh, list Drive files, send email to self).
- [ ] **Update Plan**: Schedule occasional dependency updates and quota checks.

**Optional Quick Tasks**
- [ ] **.gitignore**: Add `credentials.json`, `token.json`.
- [ ] **Example Scripts**: Add `examples/` with 2–3 scripts (send email, upload file, append sheet).
- [ ] **Local Config**: Optionally add `.env` support for credential/token paths.
- [ ] **Debug Logging Toggle**: Add one environment variable to enable debug logs.
- [ ] **License/Notes**: Add personal notes about risk of broad scopes and secrets handling.

