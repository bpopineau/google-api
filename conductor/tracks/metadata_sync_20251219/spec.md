# Specification: Local File Metadata Sync to Google Sheets

## 1. Overview
This track implements a core automation workflow: syncing local file metadata to a Google Sheet. It serves as a proof-of-concept for the "Local-to-Cloud" bridging capability of MyGoog. The user will select a local folder, and the application will extract the name, path, and last modified date of all files within that folder (non-recursive) and populate a specific Google Sheet. The process will be visible in the application's "Activity" dashboard.

## 2. User Stories
*   **As a user**, I want to select a local folder from the MyGoog interface so that I can specify which files to catalog.
*   **As a user**, I want to specify a target Google Sheet (or have one created automatically) so that the data has a destination.
*   **As a user**, I want to see the progress of the sync operation in an "Activity" dashboard so that I know the system is working.
*   **As a user**, I want the system to handle errors (e.g., file permission issues, API rate limits) gracefully without crashing the application.

## 3. Functional Requirements
### 3.1. GUI Components
*   **Folder Selector:** A standard file dialog to choose the source directory.
*   **Action Button:** A button to trigger the "Sync to Sheets" workflow.
*   **Activity Dashboard:** A new UI section (or widget) that displays a list of running/completed tasks with status icons (running, success, error).

### 3.2. Backend Logic
*   **File Scanner:** A utility to read a directory and extract `filename`, `absolute_path`, and `last_modified_timestamp` for each file.
*   **Sheets Adapter:** Extensions to the existing `mygooglib.services.sheets` module to handle batch writing (clearing old data or appending new rows).
*   **Workflow Engine:** A controller that coordinates the scanning and uploading process in a background thread to keep the UI responsive.

## 4. Non-Functional Requirements
*   **Responsiveness:** The UI must not freeze during the file scan or API upload.
*   **Error Handling:** If a single file fails to read, it should be skipped and logged, not stop the entire process.
*   **Security:** Use the existing authenticated `mygooglib` client.

## 5. Technical Constraints
*   Use `PySide6` for all UI components.
*   Use `QThread` or `QRunnable` for background processing.
*   Reuse `mygooglib` for Google API interactions.


