# Copilot instructions (google-api)

## Big picture
- **Package**: `mygooglib/` — personal-use Python library wrapping Google Drive/Sheets/Docs/Calendar/Tasks/Gmail.
- Authoritative requirements:
  - [AUTOMATION_GOALS.md](../AUTOMATION_GOALS.md) (workflows, v0.1 scope, API surface, I/O contracts)
  - [roadmap.md](../docs/development/roadmap.md) (implementation checklist and progress tracking)
  - [design_principles.md](../docs/reference/design_principles.md) (background + patterns)

## Package layout
```
mygooglib/
  __init__.py      # exposes get_creds, get_clients
  auth.py          # credential loading + OAuth flow
  client.py        # Clients dataclass + get_clients() factory
  exceptions.py    # GoogleApiError hierarchy + raise_for_http_error()
  drive.py         # upload_file, download_file, sync_folder, path resolution
  sheets.py        # get_range, update_range, append_row, spreadsheet resolution
  gmail.py         # send_email, search_messages, mark_read, attachments
  docs.py          # create, insert_text, get_text, render_template, export_pdf
  calendar.py      # add_event, list_events, update/delete events
  tasks.py         # list_tasklists, add_task, list_tasks, complete_task
  contacts.py      # basic contact operations
  workflows.py     # cross-service automation helpers
  cli/             # Typer-based CLI interface
  dashboard/       # Streamlit dashboard (optional)
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

## Development workflow
### Installation
```bash
# Install package in editable mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Install with CLI support
pip install -e ".[cli]"
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mygooglib

# Run smoke tests (read-only)
python scripts/smoke_test.py all

# Run smoke tests including writes
python scripts/smoke_test.py all --write
```

### Linting
```bash
# Format and lint with ruff
ruff check .
ruff format .
```

### CLI Usage
```bash
# See available commands
mg --help

# Example: List Drive files
mg drive list

# Example: Read from Sheets
mg sheets get --identifier "SHEET_ID" --range "Sheet1!A1:B10"
```

## Key documentation
- **[AUTOMATION_GOALS.md](../AUTOMATION_GOALS.md)**: Workflows, v0.1 scope, API surface, I/O contracts
- **[design_principles.md](../docs/reference/design_principles.md)**: Background, patterns, library strategy
- **[roadmap.md](../docs/development/roadmap.md)**: Progress tracking and implementation checklist
- **[testing.md](../docs/development/testing.md)**: Testing strategy and smoke test checklists
- **[usage guide](../docs/guides/usage.md)**: Detailed examples for all services

## Code style & conventions
- Python 3.10+ required
- Type hints encouraged but not mandatory for personal use
- Functions should be clear and self-documenting
- Prefer composition over inheritance
- Keep functions small and focused on single responsibility

