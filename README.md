# mygooglib

Personal-use Python helpers for Google Drive, Sheets, and Gmail (more services later).

## Install

```bash
pip install -e .
```

### Reproducible installs (uv)

This repo also supports a locked dependency set via `uv.lock`.

```bash
uv sync --frozen
```

To include dev extras:

```bash
uv sync --frozen --extra dev
```

## Credentials / OAuth

This library uses OAuth (Desktop app) and stores local secrets outside git.

By default (Windows), `mygooglib` looks for:

- `credentials.json`: `%LOCALAPPDATA%\mygooglib\credentials.json`
- `token.json`: `%LOCALAPPDATA%\mygooglib\token.json`

Override with env vars:

- `MYGOOGLIB_CREDENTIALS_PATH`
- `MYGOOGLIB_TOKEN_PATH`

One-time setup (creates `token.json`):

```bash
python scripts/oauth_setup.py
```

More detail: see [docs/02-credentials.md](docs/02-credentials.md).

## Quick start

```python
from mygooglib import get_clients

clients = get_clients()  # loads/refreshes token as needed
```

Aliases (equivalent):

```python
from mygooglib import create, create_clients

clients = create()
clients = create_clients()
```

### Drive

```python
from mygooglib.drive import upload_file, list_files, sync_folder

file_id = upload_file(clients.drive, "./report.pdf")
files = list_files(clients.drive, query="name contains 'report'")

# Safe sync (upload/update only; no deletes)
summary = sync_folder(clients.drive, r"C:\\path\\to\\folder", "<FOLDER_ID>")
```

### Sheets

Sheets helpers accept a spreadsheet **ID**, **title**, or full **URL**. If you pass a title, also pass `drive=clients.drive` so the library can resolve it.

```python
from mygooglib.sheets import get_range, append_row

values = get_range(
    clients.sheets,
    "Test Sheet",                 # title OR id OR url
    "Sheet1!A1:Z50",
    drive=clients.drive,           # needed for title lookup
)

append_row(
    clients.sheets,
    "Test Sheet",
    "Sheet1",
    ["a", "b", "c"],
    drive=clients.drive,
)
```

### Gmail

```python
from mygooglib.gmail import send_email, search_messages, mark_read

message_id = send_email(
    clients.gmail,
    to="you@example.com",
    subject="Hello",
    body="Sent from mygooglib",
)

results = search_messages(clients.gmail, "newer_than:7d", max_results=5)
if results:
    mark_read(clients.gmail, results[0]["id"])
```

## Smoke test runner

`scripts/smoke_test.py` provides CLI subcommands for quick manual checks.

```bash
python scripts/smoke_test.py --help
```

Run everything in one go (read-only by default):

```bash
python scripts/smoke_test.py all
```

Run everything including writes (Gmail send + Sheets write; optional Drive sync):

```bash
python scripts/smoke_test.py all --write
python scripts/smoke_test.py all --write --drive-sync-local-path "C:\\path\\to\\folder" --drive-sync-folder-id "<FOLDER_ID>"
```

## Manual smoke checklist

Run these once after OAuth setup (or any time you want a quick confidence check).

1) Confirm token refresh works (no re-consent prompt expected):

```bash
python scripts/check_token_refresh.py
```

2) Drive: list a few files (safe read-only call):

```python
from mygooglib import get_clients
from mygooglib.drive import list_files

clients = get_clients()
files = list_files(clients.drive, page_size=5)
for f in files:
    print(f["id"], f["name"])
```

3) Sheets: read a small range (use id/title/url):

```bash
python scripts/smoke_test.py sheets-get --identifier "<ID_OR_TITLE_OR_URL>" --range "Sheet1!A1:C3"
```

If `--identifier` is a title, title lookup uses Drive. Optionally scope it:

```bash
python scripts/smoke_test.py sheets-get --identifier "My Sheet" --range "Sheet1!A1:C3" --parent-id "<FOLDER_ID>"
```

4) Gmail: send to yourself + verify via search:

```bash
python scripts/smoke_test.py gmail-send --subject "mygooglib smoke" --body "Hello"
python scripts/smoke_test.py gmail-search --query "subject:mygooglib smoke newer_than:1d" --max 3
```

5) Drive: sync a local folder into a Drive folder:

```bash
python scripts/smoke_test.py drive-sync --local-path "C:\\path\\to\\folder" --drive-folder-id "<FOLDER_ID>"
```

## Notes

- The ergonomic wrappers are currently implemented as **free functions** that take the raw service objects from `get_clients()`.
- Errors are wrapped into short, actionable exceptions (see [mygooglib/exceptions.py](mygooglib/exceptions.py)).
