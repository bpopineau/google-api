# Specification: Verbose "Dry Run" Simulator

## Overview
This feature introduces a `dry_run` parameter to all destructive or modifying API operations in the library. When enabled, the operation will not be executed; instead, a structured report will be returned detailing exactly what *would* have happened. This enhances safety and allows AI agents to verify their intended actions before committing them.

## Functional Requirements

### 1. `dry_run` Parameter
- Add an optional `dry_run: bool = False` parameter to the following functions:
    - **Drive:** `delete_file`, `upload_file`, `create_folder`, `sync_folder`.
    - **Sheets:** `update_values`, `batch_update_values`, `append_values`.

### 2. Structured `DryRunReport`
- Define a `DryRunReport` TypedDict in `mygooglib/core/types.py`.
- The report must include:
    - `action`: String identifying the operation (e.g., "drive.delete").
    - `resource_id`: The ID or name of the affected resource.
    - `details`: A dictionary of proposed changes (e.g., `{ "new_name": "...", "parents": ["..."] }`).
    - `reason`: (Optional) String explaining why the action was triggered (critical for `sync_folder`).

### 3. Return Behavior
- If `dry_run=True`, functions MUST return the `DryRunReport` (or a list of reports for batch/sync operations).
- If `dry_run=False` (default), the function behavior remains unchanged.

### 4. `sync_folder` Enhancement
- Update `sync_folder` to return a list of `DryRunReport` objects representing every file/folder creation or update it would perform.

## Non-Functional Requirements
- **No Side Effects:** When `dry_run=True`, no network requests that modify state should be sent to Google APIs.
- **Type Safety:** Ensure the return type of modified functions is correctly hinted as `Union[ResultType, DryRunReport]`.

## Acceptance Criteria
- [ ] Calling `delete_file(..., dry_run=True)` does not delete the file and returns a valid report.
- [ ] `sync_folder(..., dry_run=True)` returns a detailed log of all planned file operations.
- [ ] Sheets update functions return a preview of the data to be written.
- [ ] Existing code without `dry_run` parameter continues to work without changes.

## Out of Scope
- Global "Dry Run" toggle via environment variables (per-call only for now).
- Dry run for read-only operations (unnecessary).
