# MyGoog Library Context Map

This file is auto-generated. It lists the available tools in `mygooglib`.

## Core: `mygooglib.core.client.Clients`
The main entry point factory. Accessed via `get_clients()`.

* `clients.appscript` -> Returns Service Client
* `clients.calendar` -> Returns Service Client
* `clients.contacts` -> Returns Service Client
* `clients.docs` -> Returns Service Client
* `clients.drive` -> Returns Service Client
* `clients.gmail` -> Returns Service Client
* `clients.sheets` -> Returns Service Client
* `clients.tasks` -> Returns Service Client

## Service: `AppScriptClient`
Defined in: `mygooglib.services.appscript`
```python
def run(self, script_id: 'str', function_name: 'str', parameters: 'list[Any] | None' = None, *, dev_mode: 'bool' = False) -> 'Any':
    """Execute a function in a deployed Apps Script project."""
```

## Service: `CalendarClient`
Defined in: `mygooglib.services.calendar`
```python
def add_event(self, *, summary: 'str', start: 'dt.datetime | dt.date', end: 'dt.datetime | dt.date | None' = None, duration_minutes: 'int | None' = None, description: 'str | None' = None, location: 'str | None' = None, calendar_id: 'str' = 'primary', raw: 'bool' = False) -> 'str | dict':
    """Add an event to a Google Calendar."""
def delete_event(self, event_id: 'str', *, calendar_id: 'str' = 'primary') -> 'None':
    """Delete an event from a Google Calendar."""
def list_events(self, *, calendar_id: 'str' = 'primary', time_min: 'dt.datetime | None' = None, time_max: 'dt.datetime | None' = None, max_results: 'int' = 100, raw: 'bool' = False, progress_callback: 'Any | None' = None) -> 'list[dict] | dict':
    """List events from a calendar."""
```

## Service: `ContactsClient`
Defined in: `mygooglib.services.contacts`
```python
def create_contact(self, *, given_name: 'str', family_name: 'str | None' = None, email: 'str | None' = None, phone: 'str | None' = None) -> 'dict':
    """Create a new contact."""
def delete_contact(self, resource_name: 'str') -> 'None':
    """Delete a contact."""
def get_contact(self, resource_name: 'str') -> 'dict':
    """Get a specific contact."""
def list_contacts(self, *, page_size: 'int' = 30, sort_order: 'str' = 'FIRST_NAME_ASCENDING') -> 'list[dict]':
    """List contacts."""
def search_contacts(self, query: 'str') -> 'list[dict]':
    """Search contacts."""
def update_contact(self, resource_name: 'str', *, given_name: 'str | None' = None, family_name: 'str | None' = None, email: 'str | None' = None, phone: 'str | None' = None) -> 'dict':
    """Update an existing contact."""
```

## Service: `DocsClient`
Defined in: `mygooglib.services.docs`
```python
def append_text(self, doc_id: 'str', text: 'str') -> 'None':
    """Append text to the end of a document."""
def create(self, title: 'str') -> 'str':
    """Create a new empty document."""
def export_pdf(self, doc_id: 'str', dest_path: 'str | os.PathLike') -> 'Path':
    """Export a Google Doc as a PDF."""
def find_replace(self, doc_id: 'str', replacements: 'dict[str, str]', *, match_case: 'bool' = True) -> 'int':
    """Perform multiple find-and-replace operations in a document."""
def get_text(self, doc_id: 'str') -> 'str':
    """Get all plain text from a document."""
def insert_table(self, doc_id: 'str', rows: 'list[list[str]]', *, headers: 'list[str] | None' = None, index: 'int | None' = None) -> 'int':
    """Insert a table into a document."""
def render_list(self, doc_id: 'str', tag: 'str', items: 'list[str]', *, bullet: 'str' = '• ') -> 'int':
    """Replace a placeholder tag with a bulleted list."""
def render_template(self, template_id: 'str', data: 'dict[str, str]', *, title: 'str | None' = None, raw: 'bool' = False) -> 'str | dict':
    """Create a new document from a template by replacing placeholders."""
```

## Service: `DriveClient`
Defined in: `mygooglib.services.drive`
```python
def create_folder(self, name: 'str', *, parent_id: 'str | None' = None, raw: 'bool' = False) -> 'str | dict':
    """Create a folder in Drive."""
def delete_file(self, file_id: 'str', *, permanent: 'bool' = False) -> 'None':
    """Delete a file or move it to trash."""
def download_file(self, file_id: 'str', dest_path: 'str | os.PathLike', *, export_mime_type: 'str | None' = None, progress_callback: 'Any | None' = None) -> 'Path':
    """Download a file from Drive."""
def find_by_name(self, name: 'str', *, parent_id: 'str | None' = None, mime_type: 'str | None' = None) -> 'dict | None':
    """Find first file with exact name."""
def list_files(self, *, query: 'str | None' = None, parent_id: 'str | None' = None, mime_type: 'str | None' = None, trashed: 'bool' = False, page_size: 'int' = 100, max_results: 'int | None' = None, fields: 'str' = 'id, name, mimeType, modifiedTime, size, parents') -> 'list[dict]':
    """List files matching criteria with pagination."""
def resolve_path(self, path: 'str', *, parent_id: 'str' = 'root') -> 'dict | None':
    """Resolve a human-readable path string to Drive file metadata."""
def sync_folder(self, local_path: 'str | os.PathLike', drive_folder_id: 'str', *, recursive: 'bool' = True, dry_run: 'bool' = False, progress_callback: 'Any | None' = None) -> 'dict':
    """Sync a local folder to a Drive folder."""
def upload_file(self, local_path: 'str | os.PathLike', *, parent_id: 'str | None' = None, name: 'str | None' = None, mime_type: 'str | None' = None, raw: 'bool' = False, progress_callback: 'Any | None' = None) -> 'str | dict':
    """Upload a local file to Drive."""
```

## Service: `GmailClient`
Defined in: `mygooglib.services.gmail`
```python
def archive_message(self, message_id: 'str', *, user_id: 'str' = 'me', raw: 'bool' = False) -> 'dict | None':
    """Archive a message by removing the INBOX label."""
def get_attachment(self, message_id: 'str', attachment_id: 'str', *, user_id: 'str' = 'me') -> 'bytes':
    """Download a single attachment by ID."""
def get_message(self, message_id: 'str', *, user_id: 'str' = 'me', raw: 'bool' = False) -> 'dict':
    """Get full message details including body."""
def list_labels(self, *, user_id: 'str' = 'me', raw: 'bool' = False) -> 'list[dict] | dict':
    """List all labels in the user's mailbox."""
def mark_read(self, message_id: 'str', *, user_id: 'str' = 'me', raw: 'bool' = False) -> 'dict | None':
    """Mark a message as read by removing the UNREAD label."""
def save_attachments(self, query: 'str', dest_folder: 'str | Path', *, user_id: 'str' = 'me', max_messages: 'int' = 50, filename_filter: 'str | None' = None, progress_callback: 'Any | None' = None) -> 'list[Path]':
    """Save all attachments from messages matching a query to a folder."""
def search_messages(self, query: 'str', *, user_id: 'str' = 'me', max_results: 'int' = 50, include_spam_trash: 'bool' = False, raw: 'bool' = False, progress_callback: 'Any | None' = None) -> 'list[dict] | dict':
    """Search Gmail and return lightweight message dicts."""
def send_email(self, *, to: 'str | Sequence[str]', subject: 'str', body: 'str', attachments: 'Sequence[str | Path] | None' = None, cc: 'str | Sequence[str] | None' = None, bcc: 'str | Sequence[str] | None' = None, user_id: 'str' = 'me', raw: 'bool' = False, idempotency_key: 'str | None' = None) -> 'str | dict | None':
    """Send a plain-text email with optional file attachments."""
def trash_message(self, message_id: 'str', *, user_id: 'str' = 'me', raw: 'bool' = False) -> 'dict | None':
    """Move a message to trash."""
```

## Service: `SheetsClient`
Defined in: `mygooglib.services.sheets`
```python
def append_row(self, spreadsheet_id: 'str', sheet_name: 'str', values: 'Sequence[Any]', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, value_input_option: 'str' = 'RAW', insert_data_option: 'str | None' = None, include_values_in_response: 'bool' = False, raw: 'bool' = False) -> 'dict | None':
    """Append a single row to the end of a sheet."""
def batch(self, spreadsheet_id: 'str', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, value_input_option: 'str' = 'RAW') -> 'BatchUpdater':
    """Create a batch context manager for efficient bulk updates."""
def batch_get(self, spreadsheet_id: 'str', ranges: 'list[str]', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, major_dimension: 'str | None' = None, value_render_option: 'str | None' = None, date_time_render_option: 'str | None' = None, raw: 'bool' = False) -> 'dict[str, list[list[Any]]] | dict':
    """Read multiple ranges from a spreadsheet in a single API call."""
def batch_update(self, spreadsheet_id: 'str', updates: 'list[dict[str, Any]]', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, value_input_option: 'str' = 'RAW', include_values_in_response: 'bool' = False, response_value_render_option: 'str | None' = None, response_date_time_render_option: 'str | None' = None, raw: 'bool' = False) -> 'dict':
    """Update multiple ranges in a spreadsheet in a single API call."""
def batch_write(self, spreadsheet_id: 'str', sheet_name: 'str', rows: 'Sequence[Sequence[Any]]', *, headers: 'Sequence[str] | None' = None, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, clear: 'bool' = False, start_cell: 'str' = 'A1') -> 'dict | None':
    """Write a batch of rows to a sheet, optionally clearing it first."""
def clear_sheet(self, spreadsheet_id: 'str', sheet_name: 'str', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, raw: 'bool' = False) -> 'dict | None':
    """Clear all values from a specific sheet (tab)."""
def create_spreadsheet(self, title: 'str', *, sheet_name: 'str' = 'Sheet1', raw: 'bool' = False) -> 'dict | str':
    """Create a new Google Spreadsheet."""
def exists(self, identifier: 'str') -> 'bool':
    """Check if a spreadsheet exists by ID, Title, or URL."""
def from_dataframe(self, spreadsheet_id: 'str', sheet_name: 'str', df: "'pd.DataFrame'", *, start_cell: 'str' = 'A1', include_header: 'bool' = True, include_index: 'bool' = False, resize: 'bool' = False) -> 'dict | None':
    """Write a Pandas DataFrame to a sheet."""
def get_range(self, spreadsheet_id: 'str', a1_range: 'str', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, major_dimension: 'str | None' = None, value_render_option: 'str | None' = None, date_time_render_option: 'str | None' = None, raw: 'bool' = False, chunk_size: 'int | None' = None, progress_callback: 'Any | None' = None) -> 'list[list[Any]] | dict':
    """Read a range of values from a spreadsheet."""
def get_sheets(self, spreadsheet_id: 'str', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, raw: 'bool' = False) -> 'list[dict] | dict':
    """Get metadata for all sheets (tabs) in a spreadsheet."""
def open_by_title(self, title: 'str', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False) -> 'str':
    """Find a Google Sheet by title using the Drive API."""
def resolve_spreadsheet(self, identifier: 'str', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False) -> 'str':
    """Resolve a spreadsheet identifier (ID, title, or URL) to an ID."""
def to_dataframe(self, spreadsheet_id: 'str', a1_range: 'str', *, header: 'bool' = True) -> "'pd.DataFrame'":
    """Read a range into a Pandas DataFrame."""
def update_range(self, spreadsheet_id: 'str', a1_range: 'str', values: 'Sequence[Sequence[Any]]', *, parent_id: 'str | None' = None, allow_multiple: 'bool' = False, value_input_option: 'str' = 'RAW', include_values_in_response: 'bool' = False, response_value_render_option: 'str | None' = None, response_date_time_render_option: 'str | None' = None, raw: 'bool' = False) -> 'dict | None':
    """Update a range of values in a spreadsheet."""
```

## Service: `TasksClient`
Defined in: `mygooglib.services.tasks`
```python
def add_task(self, *, title: 'str', tasklist_id: 'str' = '@default', notes: 'str | None' = None, due: 'dt.datetime | dt.date | None' = None, raw: 'bool' = False) -> 'str | dict':
    """Add a task to a task list."""
def complete_task(self, task_id: 'str', *, tasklist_id: 'str' = '@default', raw: 'bool' = False) -> 'dict | None':
    """Mark a task as completed."""
def delete_task(self, task_id: 'str', *, tasklist_id: 'str' = '@default') -> 'None':
    """Delete a task from a task list."""
def list_tasklists(self, *, max_results: 'int' = 100, raw: 'bool' = False) -> 'list[dict] | dict':
    """List the user's task lists."""
def list_tasks(self, *, tasklist_id: 'str' = '@default', show_completed: 'bool' = True, show_hidden: 'bool' = False, max_results: 'int' = 100, raw: 'bool' = False, progress_callback: 'Any | None' = None) -> 'list[dict] | dict':
    """List tasks in a task list."""
def update_task(self, task_id: 'str', *, tasklist_id: 'str' = '@default', title: 'str | None' = None, notes: 'str | None' = None, status: 'str | None' = None, due: 'dt.datetime | dt.date | None' = None, raw: 'bool' = False) -> 'dict | None':
    """Update a task's properties."""
```
