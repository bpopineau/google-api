# Track Specification: Sheets Write-Back

## Overview
Transform the Sheets page from a read-only viewer into a functional editor. This allows users to perform "Read/update a tracker" workflows directly within the MyGoog GUI, bridging the gap between viewing data and acting on it.

## Requirements

### Functional
1.  **Inline Table Editing (Update):**
    -   The `QTableWidget` in `mygoog_gui/pages/sheets.py` must allow cell editing.
    -   Implement "dirty state" tracking: a "Save Changes" button should be enabled only when cell content has changed.
    -   The "Save Changes" button will call the `update_range` backend method to push grid changes to Google Sheets.

2.  **Append Row Form:**
    -   Implement a dedicated "Append Row" section at the bottom of the Sheets page.
    -   The section will provide input fields corresponding to the sheet columns.
    -   An "Add Row" button will call the `append_row` backend method.

3.  **UI/UX:**
    -   Follow the "Professional yet Personal" tone: use clear labels and provide a friendly notification upon successful save/append.
    -   **Speed First:** Ensure cell edits and row additions don't block the UI thread (utilize existing async worker patterns).

4.  **Error Handling:**
    -   Adopt "Friendly but Direct" error messages. If a network failure occurs during save, show a dialog explaining the failure without raw stack traces.

### Non-Functional
1.  **Optimistic Validation:** Perform minimal local validation; rely on backend/API error handling for data integrity.
2.  **Persistence:** Changes are only sent to Google Sheets when the user explicitly clicks "Save Changes" or "Add Row".

## Tech Stack Alignment
*   **Language:** Python 3.10+
*   **GUI:** PySide6 (`QTableWidget`, `QLineEdit`, `QPushButton`)
*   **Library:** `mygooglib.services.sheets` (already supports `update_range` and `append_row`)

## Out of Scope
- Complex sheet features like formula editing or formatting (bold, colors, etc.).
- Schema enforcement or local data type validation.
- Multi-sheet "Batch" updates (updates are per-range/per-row).
