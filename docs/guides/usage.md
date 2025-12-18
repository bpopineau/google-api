# Usage Guide

This guide provides examples of how to use the different services provided by `mygooglib`.

## Quick Start: Getting Clients

The library provides a factory function to get all authorized service clients at once.

```python
from mygooglib import get_clients

clients = get_clients()  # loads/refreshes token as needed
# clients.drive, clients.sheets, clients.gmail are now ready
```

---

## 1. Google Drive

Drive helpers simplify file management and synchronization.

```python
from mygooglib.drive import upload_file, list_files, sync_folder

# Upload a file
file_id = upload_file(clients.drive, "./report.pdf")

# List files matching a query
files = list_files(clients.drive, query="name contains 'report'")

# Sync a local folder to a Drive folder (supports paths or IDs)
summary = sync_folder(clients.drive, r"C:\path\to\folder", "Backups/2025")
```

---

## 2. Google Sheets

Sheets helpers handle ID/Title resolution and range operations.

```python
from mygooglib.sheets import get_range, append_row

# Read a range (supports Title, ID, or URL)
# If using a Title, provide the drive client for resolution
values = get_range(
    clients.sheets,
    "Test Sheet",                 # title OR id OR url
    "Sheet1!A1:Z50",
    drive=clients.drive,           # needed for title lookup
)

# Append a row
append_row(
    clients.sheets,
    "Test Sheet",
    "Sheet1",
    ["data1", "data2", "data3"],
    drive=clients.drive,
)
```

---

## 3. Gmail

Gmail helpers handle email encoding and searching.

```python
from mygooglib.gmail import send_email, search_messages, mark_read

# Send an email with attachments
message_id = send_email(
    clients.gmail,
    to="recipient@example.com",
    subject="Hello from mygooglib",
    body="This is an automated email.",
    attachments=["./files/doc.pdf"]
)

# Search for recent messages
results = search_messages(clients.gmail, "newer_than:7d", max_results=5)

# Mark a message as read
if results:
    mark_read(clients.gmail, results[0]["id"])
```

---

## 4. Cross-Service Workflows

Workflows combine multiple services to automate complex tasks.

### Sheets to Calendar

Import events from a spreadsheet. The sheet should have columns for Summary, Start, End/Duration, and Description.

```python
from mygooglib.workflows import import_events_from_sheets

result = import_events_from_sheets(
    clients,
    spreadsheet_id="Marketing Events",
    range_name="Events!A2:D50"
)
print(f"Created {result['created']} events.")
```

---

## See Also

For more examples, check the [examples/](../../examples/) directory in the repository.
