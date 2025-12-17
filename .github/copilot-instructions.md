# Copilot instructions (google-api)

## Big picture
- **Package**: `mygooglib/` — personal-use Python library wrapping Google Drive/Sheets/Docs/Calendar/Tasks/Gmail.
- Authoritative requirements:
  - [AUTOMATION_GOALS.md](../AUTOMATION_GOALS.md) (workflows, v0.1 scope, API surface, I/O contracts)
  - [TODO.md](../TODO.md) (implementation checklist)
  - [LIBRARY_STRATEGY.md](../LIBRARY_STRATEGY.md) (background + patterns)

## Package layout
```
mygooglib/
  __init__.py      # exposes get_creds, get_clients
  auth.py          # credential loading + OAuth flow
  client.py        # Clients dataclass + get_clients() factory
  exceptions.py    # GoogleApiError hierarchy + raise_for_http_error()
  drive.py         # (stub) upload_file, download_file, sync_folder, ...
  sheets.py        # (stub) get_range, update_range, append_row
  gmail.py         # (stub) send_email, search_messages, mark_read
  docs.py / calendar.py / tasks.py  # stubs for later
  utils/
    a1.py          # col_to_a1, a1_to_col, range_to_a1
    datetime.py    # to_rfc3339, from_rfc3339, DEFAULT_TZ
```

## Quick start (after `pip install -e .`)
```python
from mygooglib import get_clients
clients = get_clients()          # uses token from default location
clients.drive   # raw Resource for Drive v3
clients.sheets  # raw Resource for Sheets v4
clients.gmail   # raw Resource for Gmail v1
```

## Product intent (don’t fight it)
- Build a **personal-use** Python library that wraps Google Drive/Sheets/Docs/Calendar/Tasks/Gmail.
- Optimize for **ergonomic, stable, small surface area** (“~12 excellent functions”) over exhaustive coverage.
- Prefer **one-liner happy paths** for the v0.1 Must workflows: Drive folder sync, Sheets read/write, Gmail send/search.

## API shape & conventions (from `AUTOMATION_GOALS.md`)
- Return **plain Python types** by default (ids, strings, lists-of-lists, small summary dicts); avoid exposing raw Google response shapes as the primary API.
- Naming is **action-oriented**: `get_range`, `append_row`, `send_email`, `search_messages`, `mark_read`, `sync_folder`.
- Sheets:
  - Row/col helpers are **1-indexed**.
  - Range-oriented methods use **A1 notation** strings.
- Calendar/Tasks:
  - Accept Python `date`/`datetime` inputs without drama; define a sane default TZ for naive datetimes.
- Gmail:
  - `send_email(..., attachments=[...])` accepts file paths; hide MIME/base64 details.
- Provide a deliberate “raw escape hatch” for advanced use (e.g., `raw=True`), but keep it opt-in.

## Auth + clients
- Design for **auth once, reuse clients**: build service clients a single time and share credentials across services.
- Prefer a small factory (e.g., `client.create()` returning typed clients/wrappers) over scattering `build()` calls.

## Errors & diagnostics
- Raise **short, actionable exceptions**; avoid turning normal failures into huge google client stack traces.
- When wrapping `HttpError`, include the HTTP status and a brief hint (auth/scopes, missing file, permissions, quota).

## Secrets & local config
- Never commit `credentials.json` / `token.json` (treat as local secrets); keep paths configurable (env var or a local config file).
- Do not print tokens/secret material in logs or error messages.
