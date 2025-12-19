# mygooglib

Personal-use Python helpers for Google Drive, Sheets, Gmail, Docs, Calendar, Tasks, and Contacts.

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure (one-time setup)
python scripts/oauth_setup.py

# 3. Use in Python
from mygooglib import get_clients
clients = get_clients()
```

## CLI Interface

```bash
pip install -e ".[cli]"
mygoog --help
```

Install optional features:
```bash
pip install -e ".[cli,data]"  # Adds Pandas support for Sheets
pip install -e ".[gui]"       # PySide6 Desktop GUI
```

---

## Documentation

- **[Configuration & Auth](docs/guides/configuration.md)**: OAuth setup and token management.
- **[Usage Guide](docs/guides/usage.md)**: API examples for all services.
- **[Roadmap](docs/development/roadmap.md)**: Progress tracking and feature ideas.

---

## Feature Overview

| Service | Key Features |
|---------|--------------|
| **Drive** | Upload, download, list, sync folders, path resolution (`"Reports/2025"`) |
| **Sheets** | Read/write ranges, batch ops, Pandas `to_dataframe()`/`from_dataframe()` |
| **Gmail** | Send with attachments, search, mark read, save attachments from search |
| **Docs** | Template rendering, tables, lists, text extraction, PDF export, find & replace |
| **Calendar** | Create/list/update events with Python `datetime` objects |
| **Tasks** | List/add/complete tasks, manage tasklists |
| **Contacts** | List, search, create, update, delete contacts (People API) |

### Utilities

- **Retry with Backoff**: Automatic retry on transient 429/5xx errors
- **Idempotency Store**: SQLite-based duplicate prevention for scripts
- **Logging**: Configurable via `MYGOOGLIB_LOG_LEVEL` environment variable

---

## Example: Cross-Service Workflow

```python
from mygooglib import get_clients
from mygooglib.workflows import import_events_from_sheets

clients = get_clients()
result = import_events_from_sheets(
    clients,
    spreadsheet_id="Event Planning",
    range_name="Events!A2:D50"
)
print(f"Created {result['created']} calendar events")
```

---

For complete API details, see the **[Usage Guide](docs/guides/usage.md)**.
