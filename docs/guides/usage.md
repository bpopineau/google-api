# Usage Guide

This guide provides examples of how to use the different services provided by `mygooglib`.

## Quick Start: Getting Clients

The library provides a factory function to get all authorized service clients at once.
Services are lazily initialized — only built when first accessed.

```python
from mygooglib import get_clients

clients = get_clients()  # loads/refreshes token as needed
# clients.drive, clients.sheets, clients.gmail, clients.calendar,
# clients.tasks, clients.docs, clients.contacts are now available
```

---

## 1. Google Drive

Drive helpers simplify file management and synchronization.

```python
# Upload a file
file_id = clients.drive.upload_file("./report.pdf")

# List files matching a query
files = clients.drive.list_files(query="name contains 'report'")

# Download a file
clients.drive.download_file(file_id, "./downloads/report.pdf")

# Sync a local folder to a Drive folder (supports paths or IDs)
summary = clients.drive.sync_folder(r"C:\path\to\folder", "Backups/2025")
```

---

## 2. Google Sheets

Sheets helpers handle ID/Title resolution and range operations.

```python
# Read a range (supports Title, ID, or URL)
values = clients.sheets.get_range("Test Sheet", "Sheet1!A1:Z50")

# Append a row
clients.sheets.append_row("Test Sheet", "Sheet1", ["data1", "data2", "data3"])

# Batch get multiple ranges in one API call
data = clients.sheets.batch_get("my_sheet_id", ["Sheet1!A:A", "Sheet2!B:C"])

# Batch update multiple ranges
clients.sheets.batch_update("my_sheet_id", [
    {"range": "A1:B2", "values": [[1, 2], [3, 4]]},
    {"range": "C1:D2", "values": [[5, 6], [7, 8]]}
])
```

### Pandas Integration

Requires `pip install -e ".[data]"`:

```python
# Read range as DataFrame
df = clients.sheets.to_dataframe("Test Sheet", "Data!A1:E100")

# Write DataFrame to sheet
clients.sheets.from_dataframe("Test Sheet", "Output", df)
```

---

## 3. Gmail

Gmail helpers handle email encoding, searching, and attachments.

```python
# Send an email with attachments
message_id = clients.gmail.send_email(
    to="recipient@example.com",
    subject="Hello from mygooglib",
    body="This is an automated email.",
    attachments=["./files/doc.pdf"]
)

# Search for recent messages
results = clients.gmail.search_messages("newer_than:7d", max_results=5)

# Mark a message as read
clients.gmail.mark_read(results[0]["id"])

# Save all attachments from search results
saved_files = clients.gmail.save_attachments(
    "from:invoices@company.com has:attachment",
    "./downloads/invoices/"
)
```

### Idempotent Email Sending

Prevent duplicate sends with an idempotency key:

```python
clients.gmail.send_email(
    to="user@example.com",
    subject="Daily Report",
    body="...",
    idempotency_key="daily-report-2025-12-19"  # Won't send if already processed
)
```

---

## 4. Google Docs

```python
# Create a new document
doc_id = clients.docs.create("My New Document")

# Get document text
text = clients.docs.get_text(doc_id)

# Render a template (placeholders like {{name}})
new_doc_id = clients.docs.render_template(
    template_id="abc123",
    data={"name": "John", "date": "Dec 19, 2025"}
)

# Find and replace text
count = clients.docs.find_replace(doc_id, {"old_text": "new_text"})

# Export to PDF
clients.docs.export_pdf(doc_id, "./output.pdf")

# Insert a table from data
clients.docs.insert_table(doc_id, [
    ["Alice", "95"],
    ["Bob", "87"],
], headers=["Name", "Score"])

# Replace a placeholder with a bulleted list
clients.docs.render_list(doc_id, "{{ITEMS}}", ["Item 1", "Item 2", "Item 3"])
```

---

## 5. Google Calendar

```python
from datetime import datetime, timedelta

# Add an event
event_id = clients.calendar.add_event(
    summary="Team Meeting",
    start=datetime(2025, 12, 20, 10, 0),
    end=datetime(2025, 12, 20, 11, 0),
    description="Weekly sync"
)

# List upcoming events
events = clients.calendar.list_events(max_results=10)

# Update an event
clients.calendar.update_event(event_id, summary="Updated Meeting Title")

# Delete an event
clients.calendar.delete_event(event_id)
```

---

## 6. Google Tasks

```python
# List all task lists
tasklists = clients.tasks.list_tasklists()

# Add a task
task_id = clients.tasks.add_task(
    "Buy groceries",
    notes="Milk, eggs, bread",
    due=datetime(2025, 12, 20)
)

# List tasks in a tasklist
tasks = clients.tasks.list_tasks()

# Complete a task
clients.tasks.complete_task(task_id)
```

---

## 7. Google Contacts (People API)

```python
# List contacts
contacts = clients.contacts.list_contacts(page_size=50)

# Search contacts
results = clients.contacts.search_contacts("john")

# Create a new contact
contact = clients.contacts.create_contact(
    given_name="Jane",
    family_name="Doe",
    email="jane@example.com",
    phone="+1-555-1234"
)

# Update a contact
clients.contacts.update_contact(
    contact["resourceName"],
    email="jane.new@example.com"
)

# Delete a contact
clients.contacts.delete_contact(contact["resourceName"])
```

---

## 8. Cross-Service Workflows

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

## 9. Idempotency for Scripts

Prevent duplicate operations when running scripts multiple times:

```python
from mygooglib.utils.idempotency import IdempotencyStore, idempotent

store = IdempotencyStore()  # Uses ~/.mygooglib/idempotency.db

# Check if already processed
if not store.check("unique-operation-key"):
    # Do the work
    store.add("unique-operation-key")

# Or use the decorator
@idempotent(key_func=lambda row: f"process-row-{row['id']}")
def process_row(row):
    # This only runs once per unique key
    ...
```

---

## CLI Reference

Common CLI commands:

```bash
# Drive
mygoog drive list --query "name contains 'report'"
mygoog drive upload ./file.pdf
mygoog drive sync ./local/folder "Remote/Path"

# Sheets
mygoog sheets get "My Sheet" "Sheet1!A1:C10"
mygoog sheets append "My Sheet" "Sheet1" "val1" "val2"
mygoog sheets to-df "My Sheet" "Data!A:Z"  # Requires pandas

# Gmail
mygoog gmail send --to user@example.com --subject "Test" --body "Hello"
mygoog gmail search "newer_than:1d"
mygoog gmail save-attachments --query "has:attachment" --dest ./downloads

# Calendar
mygoog calendar list
mygoog calendar add "Meeting" --start "2025-12-20 10:00"

# Tasks
mygoog tasks list
mygoog tasks add "Buy groceries"
mygoog tasks complete <task_id>

# Contacts
mygoog contacts list
mygoog contacts search "john"
mygoog contacts add --given-name John --email john@example.com
```

---

---

## 10. Desktop GUI

The library includes a native PySide6 desktop application for managing your services.

### Installation

The GUI requires additional dependencies:

```bash
pip install -e ".[gui]"
```

### Launching

Run the GUI from the command line:

```bash
mygoog gui run
```

### Features

- **Dashboard**: Overview of connected services
- **Drive**: Browser-like file explorer
- **Gmail**: Read and send emails with attachments
- **Tasks**: Manage to-do lists drag-and-drop
- **Calendar**: View upcoming events
- **Dark Mode**: Integrated dark theme

---

## See Also

For more examples, check the [examples/](../../examples/) directory in the repository.
