# mygooglib

Personal-use Python helpers for Google Drive, Sheets, and Gmail (more services later).

## Install

```bash
pip install -e .
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

### Drive

```python
from mygooglib.drive import upload_file, list_files

file_id = upload_file(clients.drive, "./report.pdf")
files = list_files(clients.drive, query="name contains 'report'")
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

## Notes

- The ergonomic wrappers are currently implemented as **free functions** that take the raw service objects from `get_clients()`.
- Errors are wrapped into short, actionable exceptions (see [mygooglib/exceptions.py](mygooglib/exceptions.py)).
