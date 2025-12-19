# Plan: Local File Metadata Sync to Google Sheets

## Phase 1: Backend Foundation
- [ ] Task: Create `FileScanner` utility in `mygooglib.utils` to extract metadata (name, path, modified date).
    - [ ] Subtask: Write unit tests for `FileScanner` covering standard files and edge cases (empty folders, permission errors).
    - [ ] Subtask: Implement `FileScanner` class.
- [ ] Task: Extend `mygooglib.sheets` with `batch_write` capability.
    - [ ] Subtask: Write integration tests for `batch_write` using a mock or test Sheet.
    - [ ] Subtask: Implement `batch_write` method to accept a list of headers and rows.
- [ ] Task: Conductor - User Manual Verification 'Backend Foundation' (Protocol in workflow.md)

## Phase 2: GUI Implementation - Activity Dashboard
- [ ] Task: Create `ActivityModel` and `ActivityWidget` in `mygooglib.gui.widgets`.
    - [ ] Subtask: Design the `ActivityModel` (QAbstractListModel) to store task status.
    - [ ] Subtask: Implement `ActivityWidget` to display the list of activities with icons.
- [ ] Task: Integrate `ActivityWidget` into the main application layout.
    - [ ] Subtask: Add the widget to the sidebar or a new tab in `mygooglib.gui.main`.
- [ ] Task: Conductor - User Manual Verification 'GUI Implementation - Activity Dashboard' (Protocol in workflow.md)

## Phase 3: Workflow Integration
- [ ] Task: Implement `SyncWorker` (QThread/QRunnable) to coordinate scanning and uploading.
    - [ ] Subtask: Write tests for `SyncWorker` signals (started, progress, finished, error).
    - [ ] Subtask: Implement the worker logic to use `FileScanner` and `mygooglib.sheets`.
- [ ] Task: Add UI controls for the Sync Workflow.
    - [ ] Subtask: Add a "Sync Folder to Sheets" button in the GUI (likely in a "Tools" or "Drive" section).
    - [ ] Subtask: Connect the button to a folder selection dialog and then start the `SyncWorker`.
- [ ] Task: Conductor - User Manual Verification 'Workflow Integration' (Protocol in workflow.md)
