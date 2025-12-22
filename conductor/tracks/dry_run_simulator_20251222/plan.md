# Plan: Verbose "Dry Run" Simulator

Implementation of a structured dry-run reporting system for destructive and modifying API operations in `mygooglib`.

## Phase 1: Foundation and Shared Logic
- [x] Task: Define `DryRunReport` TypedDict in `mygooglib/core/types.py`.
- [x] Task: Create `tests/test_dry_run_foundation.py` to verify report structure.
- [x] Task: Implement a helper or base logic in `mygooglib/core/utils/base.py` (or similar) to handle the dry-run return pattern.
- [x] Task: Conductor - User Manual Verification 'Foundation and Shared Logic' (Protocol in workflow.md)

## Phase 2: Drive API Implementation
- [x] Task: Add `dry_run` support to `mygooglib/services/drive.py`: `delete_file`.
- [x] Task: Add `dry_run` support to `mygooglib/services/drive.py`: `upload_file` and `create_folder`.
- [x] Task: Implement unit tests in `tests/services/test_drive_dry_run.py` (mocking Google API calls).
- [x] Task: Conductor - User Manual Verification 'Drive API Implementation' (Protocol in workflow.md)

## Phase 3: Sheets API Implementation
- [x] Task: Add `dry_run` support to `mygooglib/services/sheets.py`: `update_values` and `batch_update_values`.
- [x] Task: Add `dry_run` support to `mygooglib/services/sheets.py`: `append_values`.
- [x] Task: Implement unit tests in `tests/services/test_sheets_dry_run.py`.
- [ ] Task: Conductor - User Manual Verification 'Sheets API Implementation' (Protocol in workflow.md)

## Phase 4: Sync Enhancement and Integration
- [ ] Task: Update `sync_folder` in `mygooglib/services/drive.py` to return a list of `DryRunReport` objects.
- [ ] Task: Update `sync_folder` tests to verify the detailed report instead of just counts.
- [ ] Task: Perform final smoke test of all dry-run enabled functions.
- [ ] Task: Conductor - User Manual Verification 'Sync Enhancement and Integration' (Protocol in workflow.md)
