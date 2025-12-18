# mygooglib

Personal-use Python helpers for Google Drive, Sheets, Gmail, Docs, Calendar, and Tasks.

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

---

## Documentation

- **[Configuration & Auth](docs/guides/configuration.md)**: How to set up Google Cloud and local secrets.
- **[Usage Guide](docs/guides/usage.md)**: Detailed examples for Drive, Sheets, Gmail, and more.
- **[Design Principles](docs/reference/design_principles.md)**: Foundational architecture and engineering strategy.
- **[Testing](docs/development/testing.md)**: Automated tests and manual smoke test checklists.
- **[Roadmap](docs/development/roadmap.md)**: Progress tracking and future feature ideas.

## Feature Overview

- **Google Drive**: File upload/download, name-based search, folder sync.
- **Google Sheets**: Title/ID/URL resolution, row/column/A1 operations, batch updates.
- **Gmail**: Robust email sending with attachments, search parsing, mark-read.
- **Docs**: Template rendering (JSON/File support), text extraction, PDF export.
- **Calendar & Tasks**: ISO-8601 aware event creation, tasklist management.
- **Maintenance**: Built-in retries for transient errors, rich logging.

---

For complete details on all modules and methods, see the **[Usage Guide](docs/guides/usage.md)**.
