# mygooglib/services

## Purpose
Contains specialized wrappers for individual Google Workspace APIs. Each module corresponds to a specific Google service (e.g., Gmail, Sheets, Drive) and provides a developer-friendly, type-safe interface over the raw Google API client.

## Key Entry Points
- [`gmail.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/services/gmail.py): High-level operations for Gmail labels, messages, and drafts.
- [`sheets.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/services/sheets.py): Operations for reading/writing spreadsheets and formatting.
- [`drive.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/services/drive.py): File management, folder creation, and permission handling.
- [`calendar.py`](file:///c:/Users/brand/Projects/google-api/mygooglib/services/calendar.py): Event management and calendar operations.

## Dependencies
- **External:** `google-api-python-client`
- **Internal:** `mygooglib.core` (for authentication and base clients)
