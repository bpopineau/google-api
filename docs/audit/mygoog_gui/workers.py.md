# Audit Report: mygoog_gui/workers.py

## Purpose
- Background workers (`QThread`) for long-running API operations to maintain UI responsiveness.

## Main Exports
- `ApiWorker`: Generic worker for single API calls.
- `BatchApiWorker`: Worker for processing lists of items with progress signals.
- `SyncWorker`: Specialized worker for local-to-Sheets file metadata synchronization.

## Findings
- **Robustness:** `SyncWorker` includes logic to ensure the target spreadsheet exists (creating it if necessary), addressing a previous requirement for graceful failure handling.
- **Reporting:** Implements descriptive signals (`started_scan`, `started_upload`, `progress`) that allow the UI to provide detailed feedback.
- **Best Practices:** Encapsulates API calls safely within `run()` methods, with exception catching and signal emission to the main thread.

## Quality Checklist
- [x] Proper QThread implementation
- [x] Detailed progress reporting
- [x] Includes "Create if Missing" logic for sync
