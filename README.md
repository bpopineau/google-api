# MyGoog: Google Workspace Desktop Manager

**MyGoog** is a desktop application for managing your Google Workspace life. It brings your Drive, Gmail, Calendar, Tasks, and Sheets together in a unified, fast, and hackable interface.

> **For Developers**: mg is also a powerful Python library. See the [Developer Guide](#developer-library) below.

## Quick Start (Desktop App)

1.  **Install**:
    ```bash
    pip install -e ".[gui]"
    ```
2.  **Launch**:
    ```bash
    mgui
    ```
    *The App will open immediately. On first run, it will open your browser to authenticate with Google.*

## Key Features

- **⚡ Instant Startup**: Launches instantly, verifying credentials in the background.
- **🎨 Modern UI**: Clean, dark-mode interface built with PySide6.
- **📂 Drive Explorer**: Browse, search, and manage files without waiting for a browser to load.
- **📧 Gmail Actions**: Rapidly triage emails (Mark Read, Trash, Archive).
- **📅 Calendar & Tasks**: View your schedule and to-dos side-by-side.

## App Documentation

- **[User Guide](docs/guides/app_user_guide.md)**: Full walkthrough of the GUI features.
- **[Configuration](docs/guides/configuration.md)**: Settings, Themes, and Auth management.

---

## <a name="developer-library"></a>Developer Library

Under the hood, `mygoog` is built on `mygooglib`, a comprehensive wrapper for Google APIs.

### Installation for Scripting

```bash
pip install -e .
```

### Usage Example

```python
from mygooglib import get_clients

# Initialize clients (handles Auth automatically)
clients = get_clients()

# List first 10 files in Drive
files = clients.drive.list_files(page_size=10)
for f in files:
    print(f"{f['name']} ({f['id']})")

# Create a Calendar Event
clients.calendar.create_event(
    summary="Code Review",
    start_time="2025-12-20T10:00:00",
    duration_minutes=45
)
```

### Library Documentation

- **[API Reference](docs/guides/usage.md)**: Detailed Python API usage.
- **[Roadmap](docs/development/roadmap.md)**: Future plans and contribution opportunities.

