# New Feature Ideas for mygooglib

This document outlines potential new features to enhance the `mygooglib` library for personal automation.

## 1. Pandas Integration for Sheets
Add `to_dataframe()` and `from_dataframe()` methods to the `SheetsClient`.

*   **Why:** Most Python users doing data automation eventually reach for Pandas. Being able to read a sheet directly into a DataFrame or write a DataFrame back to a sheet in one line would make the library a powerful tool for personal finance tracking and data analysis.
*   **Implementation:** Use `get_all_values()` to populate a DataFrame and `update_range()` to write one back, handling header rows automatically.

## 2. Batch Update Context Manager for Sheets
Implement a `with sheets.batch(spreadsheet_id) as batch:` context manager.

*   **Why:** Making many separate `update_range` calls is slow and consumes API quota quickly. A context manager could collect all requested changes and send them as a single `spreadsheets.batchUpdate` request when the block exits.
*   **Implementation:** Create a collector object that stores `ValueRange` objects and executes a single batch call in the `__exit__` method.

## 3. Cross-Service "Workflows" Module
Create a `mygooglib.workflows` module for high-level, multi-service recipes.

*   **Why:** The real power of this library is having all Google services in one place. Pre-built "recipes" would make complex automations trivial.
*   **Examples:**
    *   `sync_tasks_to_calendar()`: Automatically create Calendar events for any Google Task that has a due date.
    *   `email_sheet_as_pdf()`: Export a specific Sheet tab as a PDF (via Drive export) and immediately email it to a recipient.
    *   `log_gmail_to_sheets()`: Search for specific emails (e.g., "Order Confirmation") and append their details (date, amount, vendor) to a tracking spreadsheet.
// ...existing code...
    *   `log_gmail_to_sheets()`: Search for specific emails (e.g., "Order Confirmation") and append their details (date, amount, vendor) to a tracking spreadsheet.

## 4. Automated Gmail Attachment Management
Add a `download_attachments(message_id, save_dir)` method and a high-level `save_attachments_by_query(query, save_dir)` helper.

*   **Why:** A classic automation use case is "Save all invoices from my email to a specific folder." Currently, the library can search for messages but requires manual work to extract and save attachments.
*   **Implementation:** Extend `get_message` to handle attachment parts and write them to the local filesystem using `mimetypes` for proper extension handling.

## 5. Google People (Contacts) API Support
Add a `contacts.py` module to wrap the Google People API.

*   **Why:** Automation often requires looking up email addresses by name (e.g., "Send this to 'Mom'") or managing contact groups (e.g., "Add all these new clients to the 'Newsletter' contact group").
*   **Implementation:** `get_contact(name)`, `create_contact(email, phone)`, and `list_contacts(group)`.

## 6. Apps Script Bridge
Add a `script.py` module to execute Google Apps Script functions.

*   **Why:** Some things are still easier or only possible in Apps Script (like interacting with active spreadsheet UIs or triggering internal Google add-ons). This allows Python to "hand off" a task to an existing Apps Script project.
*   **Implementation:** Wrap the `scripts.run` endpoint to call a specific function in a deployed script project.
// filepath: c:\Users\brand\Projects\google-api\docs\NewFeatureIdeas.md
// ...existing code...
    *   `log_gmail_to_sheets()`: Search for specific emails (e.g., "Order Confirmation") and append their details (date, amount, vendor) to a tracking spreadsheet.

## 4. Automated Gmail Attachment Management
Add a `download_attachments(message_id, save_dir)` method and a high-level `save_attachments_by_query(query, save_dir)` helper.

*   **Why:** A classic automation use case is "Save all invoices from my email to a specific folder." Currently, the library can search for messages but requires manual work to extract and save attachments.
*   **Implementation:** Extend `get_message` to handle attachment parts and write them to the local filesystem using `mimetypes` for proper extension handling.

## 5. Google People (Contacts) API Support
Add a `contacts.py` module to wrap the Google People API.

*   **Why:** Automation often requires looking up email addresses by name (e.g., "Send this to 'Mom'") or managing contact groups (e.g., "Add all these new clients to the 'Newsletter' contact group").
*   **Implementation:** `get_contact(name)`, `create_contact(email, phone)`, and `list_contacts(group)`.

## 6. Apps Script Bridge
Add a `script.py` module to execute Google Apps Script functions.

*   **Why:** Some things are still easier or only possible in Apps Script (like interacting with active spreadsheet UIs or triggering internal Google add-ons). This allows Python to "hand off" a task to an existing Apps Script project.
*   **Implementation:** Wrap the `scripts.run` endpoint to call a specific function in a deployed script project.