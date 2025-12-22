# Plan: Local File Metadata Sync to Google Sheets

## Phase 1: Backend Foundation [checkpoint: 424d6c6]
- [x] Task: Create `FileScanner` utility in `mygooglib.core.utils` to extract metadata (name, path, modified date). [713becf]
    - [x] Subtask: Write unit tests for `FileScanner` covering standard files and edge cases (empty folders, permission errors).
    - [x] Subtask: Implement `FileScanner` class.
- [x] Task: Extend `mygooglib.services.sheets` with `batch_write` capability. [d2c1968]
    - [x] Subtask: Write integration tests for `batch_write` using a mock or test Sheet.
    - [x] Subtask: Implement `batch_write` method to accept a list of headers and rows.
- [x] Task: Conductor - User Manual Verification 'Backend Foundation' (Protocol in workflow.md)

## Phase 2: GUI Implementation - Activity Dashboard [checkpoint: 9194750]
- [x] Task: Create `ActivityModel` and `ActivityWidget` in `mygoog_gui.widgets`. [00ff33a]
    - [x] Subtask: Design the `ActivityModel` (QAbstractListModel) to store task status.
    - [x] Subtask: Implement `ActivityWidget` to display the list of activities with icons.
- [x] Task: Integrate `ActivityWidget` into the main application layout. [00ff33a]
    - [x] Subtask: Add the widget to the sidebar or a new tab in `mygoog_gui.main`.
- [x] Task: Conductor - User Manual Verification 'GUI Implementation - Activity Dashboard' (Protocol in workflow.md)

## Phase 3: Workflow Integration
- [x] Task: Implement `SyncWorker` (QThread/QRunnable) to coordinate scanning and uploading. [fb2fe6c]
    - [x] Subtask: Write tests for `SyncWorker` signals (started, progress, finished, error).
    - [x] Subtask: Implement the worker logic to use `FileScanner` and `mygooglib.services.sheets`.
- [x] Task: Add UI controls for the Sync Workflow. [0e99f15]
    - [x] Subtask: Add a "Sync Folder to Sheets" button in the GUI (likely in a "Tools" or "Drive" section).
    - [x] Subtask: Connect the button to a folder selection dialog and then start the `SyncWorker`.
- [x] Task: Conductor - User Manual Verification 'Workflow Integration' (Protocol in workflow.md)


