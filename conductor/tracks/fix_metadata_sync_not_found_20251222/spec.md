# Specification: Fix Metadata Sync Spreadsheet Not Found Error

## Goal
The goal of this track is to resolve a "Not found: Requested entity was not found" error that occurs during the "Local File Metadata Sync to Google Sheets" process. This error typically happens when the automation attempts to clear or write to a target Google Sheet that does not exist.

## User Story
As a user, I want the Metadata Sync workflow to automatically create the target Google Sheet if it's missing, so that the sync process can complete without manual intervention or crashing.

## Acceptance Criteria
- [ ] If the target spreadsheet ID or name does not exist, the system should create a new one.
- [ ] The `clear_sheet` operation should not fail with "Not found" if the sheet is missing; it should either handle the error or ensure existence first.
- [ ] The sync workflow completes successfully even if starting from a fresh state (no target sheet).
- [ ] Appropriate logs/status updates are provided to the user in the Activity Dashboard.

## Technical Constraints
- Follow the existing TDD rules in `workflow.md`.
- Use `mygooglib.sheets.SheetsClient` for all Sheets operations.
- Maintain compatibility with the `SyncWorker` and `ActivityWidget`.

## Out of Scope
- Redesigning the entire Sheets Client.
- Changing the metadata format being synced.

## Dependencies
- `mygooglib.sheets`
- `metadata_sync_20251219` (the previous track)
