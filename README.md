# goog - A Pythonic Google APIs Library

A personal-use Python library that provides intuitive, high-level interfaces for Google APIs.

## Supported Services

- **Drive** - File upload, download, and management
- **Sheets** - Spreadsheet reading and writing
- **Docs** - Document creation and editing
- **Calendar** - Event management
- **Tasks** - To-do list management
- **Gmail** - Email sending and searching

## Installation

```bash
pip install -e .
```

## Quick Start

### Authentication

First, download OAuth credentials from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) and save as `credentials.json`.

```python
from goog import create_clients

# Create all clients at once
clients = create_clients()
drive = clients['drive']
gmail = clients['gmail']
# etc.
```

Or initialize individual clients:

```python
from goog import GoogleAuth, DriveClient

auth = GoogleAuth()
drive = DriveClient(auth)
```

### Examples

**Upload a file to Drive:**
```python
file_id = drive.upload_file("report.pdf", name="Monthly Report")
```

**Read from Sheets:**
```python
from goog import GoogleAuth, SheetsClient

sheets = SheetsClient(GoogleAuth())
ss = sheets.open_by_id("spreadsheet_id")
ws = ss[0]  # First worksheet
data = ws.get_all_values()
```

**Send an email:**
```python
gmail.send_email(
    to="friend@example.com",
    subject="Hello!",
    body="How are you?",
    attachments=["report.pdf"]
)
```

**Create a calendar event:**
```python
from datetime import datetime
from goog import GoogleAuth, CalendarClient

calendar = CalendarClient(GoogleAuth())
calendar.add_event(
    summary="Team Meeting",
    start=datetime(2024, 1, 15, 14, 0),
    duration_minutes=60
)
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy goog/
```

## License

MIT
