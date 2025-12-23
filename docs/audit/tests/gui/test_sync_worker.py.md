# Audit Report: tests/gui/test_sync_worker.py

## Purpose
- Integration tests for the `SyncWorker` class.

## Findings
- **Async Pattern:** Correctly uses `qtbot.waitSignals` to handle multiple sequential signals (`started_scan` -> `started_upload` -> `finished`).
- **Data Integrity:** Verifies that the correct file metadata (rows) is gathered and passed to the Sheets `batch_write` API.
- **Error Handling:** Confirms that exceptions in the scanner are correctly caught and re-emitted via the `error` signal.

## Quality Checklist
- [x] Signal lifecycle verified
- [x] Error propagation tested
