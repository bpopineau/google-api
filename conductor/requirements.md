# Personal Automation Goals (Google Integrations Suite)

This file defines *what the library must make easy* before we write any code.

## 0) Scope (initial)
Services in scope:
- Google Drive
- Google Sheets
- Google Docs
- Google Calendar
- Google Tasks
- Gmail

Design intent:
- Personal-use automation
- Minimal surface area
- “One-liner” happy paths for the stuff I do repeatedly

## 1) Principles (guardrails)
- **Ergonomic > exhaustive:** prefer 12 excellent functions over 120 thin wrappers.
- **Stable interfaces:** avoid exposing raw Google API request/response shapes as the main API.
- **Composability:** small primitives + a few “workflow” helpers that combine services.
- **Fast start:** auth once, reuse clients, sane defaults.

## 2) My top workflows (v0 list)
> Edit these freely. We’ll build the library around the top 3–5 first.

### W1 — Drive: “Drop folder backup”
- Trigger: manual or scheduled
- Input: local folder path
- Output: Drive folder kept in sync (upload new/changed, optional delete handling later)
- Services: Drive
- Frequency: weekly / daily
- Success: `drive.sync_folder(local, drive_folder_id)` just works

### W2 — Sheets: “Read/update a tracker”
- Trigger: script run
- Input: spreadsheet (by id or by title), sheet/tab name, range or row append
- Output: values returned as plain Python types; updates are simple calls
- Services: Sheets
- Frequency: often
- Success: `sheets.append_row(...)`, `sheets.get_range(...)`, `sheets.update_range(...)`

### W3 — Docs: “Generate a doc from data”
- Trigger: script run
- Input: template doc id + dict of replacements + optional insert blocks
- Output: new doc id + link; optionally export to PDF
- Services: Docs (+ Drive for export)
- Frequency: monthly / as-needed
- Success: `docs.render_template(template_id, data)` and `docs.export_pdf(doc_id)`

### W4 — Calendar: “Create events from structured data”
- Trigger: script run (often reading from Sheets)
- Input: summary, start datetime/date, duration or end, timezone default
- Output: event created; returns event id + link
- Services: Calendar
- Frequency: as-needed
- Success: `cal.add_event(...)` accepts Python `date/datetime` without drama

### W5 — Tasks: “Capture tasks + triage”
- Trigger: script run / quick capture
- Input: title, notes, due (optional), list name (optional)
- Output: task created; list/search tasks
- Services: Tasks
- Frequency: often
- Success: `tasks.add("Buy ___", due=date(...))` and `tasks.list(...)`

### W6 — Gmail: “Send a clean email + attachments”
- Trigger: script run (notifications, sending reports)
- Input: to, subject, body, attachments (paths)
- Output: message sent; returns message id
- Services: Gmail
- Frequency: as-needed
- Success: `gmail.send_email(to=..., subject=..., body=..., attachments=[...])` with no MIME/base64 nonsense exposed

## 3) “Core actions” per service (what we’ll wrap first)
Drive:
- upload_file, download_file
- list(query=...), find_by_name(...)
- create_folder
Sheets:
- get_range, update_range, append_row
Docs:
- create, get_text
- find_replace, append_text
- export_pdf
Calendar:
- add_event, list_events
Tasks:
- list_tasklists, add_task, list_tasks, complete_task
Gmail:
- send_email
- search_messages (returns lightweight objects with subject/sender/snippet)
- mark_read

## 4) Non-goals (v0)
- Full coverage of every API endpoint
- Admin/domain-wide delegation flows
- A GUI
- Multi-user packaging polish (PyPI release) until the API feels “done”

## 5) MVP acceptance criteria
The library is “worth it” if:
- I can authenticate once and run scripts repeatedly without re-consenting
- Each workflow above is achievable with ~1–5 lines of code
- Errors are understandable (actionable message, not a 200-line stack trace)
- It’s easy to extend with a new helper when I discover a new repetitive task

## 6) Priority order (current guess)
1) Auth + client factory (enables everything)
2) Drive + Sheets primitives
3) Gmail send + search
4) Calendar + Tasks
5) Docs templating + export
6) Cross-service workflows (Sheets → Calendar, Sheets → Doc → Gmail, etc.)

## 7) v0.1 focus (what we build first)

Initial focus (top 3):
- W1 — Drive: Drop folder backup
- W2 — Sheets: Read/update a tracker
- W6 — Gmail: Send a clean email + attachments

Then (next 2):
- W4 — Calendar: Create events from structured data
- W5 — Tasks: Capture tasks + triage

Later:
- W3 — Docs: Generate a doc from data

## 8) Must / Nice / Later map

- Must: W1, W2, W6
- Nice: W4, W5
- Later: W3

## 9) v0.1 public API surface (keep it small)

Goal: ~12 excellent functions, not 120 thin wrappers.

Auth/Factory (Must):
- `auth.get_creds()`
- `client.get_clients()` returning typed clients
	- also available as `mygooglib.create()` / `mygooglib.create_clients()` aliases

Drive (Must):
- `upload_file(...)`
- `download_file(...)`
- `list(query=...)`
- `find_by_name(...)`
- `create_folder(...)`
- `sync_folder(local_path, drive_folder_id)`

Sheets (Must):
- `get_range(...)`
- `update_range(...)`
- `append_row(...)`

Gmail (Must):
- `send_email(to, subject, body, attachments=[])`
- `search_messages(query)`
- `mark_read(message_id)`

Calendar (Nice):
- `add_event(...)`
- `list_events(...)`

Tasks (Nice):
- `list_tasklists()`
- `add_task(...)`
- `list_tasks(...)`
- `complete_task(...)`

Docs (Later):
- `render_template(template_id, data)`
- `export_pdf(doc_id)`

## 10) Happy path contracts (inputs/outputs)

Design: return plain Python types by default; avoid raw Google response shapes.

Drive sync (W1):
- Input: `local_path` (str/PathLike), `drive_folder_id` (str)
- Output: summary dict (e.g., counts for created/updated/skipped + list of errors)

Sheets (W2):
- Inputs: spreadsheet identifier (id OR title), `tab_name`, `a1_range`, `values`
- Outputs:
	- reads return list-of-lists (or list) of plain Python scalars
	- writes return a small dict (updated range/rows) or `None`

Docs (W3):
- Inputs: `template_id`, `data: dict[str, str]` (+ optional insert blocks)
- Outputs: `doc_id` (+ optional link); exports return a local file path

Calendar (W4):
- Inputs: `date`/`datetime` (accept naive with default TZ) + `duration` or `end`
- Outputs: `event_id` (+ optional link)

Tasks (W5):
- Inputs: title, notes, due (optional), list name/id (optional)
- Outputs: `task_id` for creates; listing returns simplified task dicts

Gmail (W6):
- Inputs: to/subject/body/attachments (paths)
- Outputs: `message_id` (+ optional link)

## 11) Naming + shape decisions

- Naming style: action-oriented and explicit where helpful (`get_range`, `append_row`, `send_email`, `search_messages`, `mark_read`)
- Sheets indexing:
	- row/col helper methods are 1-indexed
	- range-oriented methods use A1 notation strings
- Raw escape hatch: allow `raw=True` (or similar) on advanced calls where it helps
- Errors:
	- raise short, actionable exceptions by default
	- avoid dumping full google client stack traces as “normal” output

## 12) Step 1 sign-off (definition of done)

Step 1 is “done” when:
- Auth once; subsequent runs do not re-consent
- Each Must workflow is achievable in ~1–5 lines of code
- Errors are understandable and actionable
- Adding a new helper does not require refactoring existing scripts

