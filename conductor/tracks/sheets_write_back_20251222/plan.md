# Track Plan: Sheets Write-Back

## Phase 1: Update Functionality (Inline Editing)
This phase enables users to edit existing cells and save changes back to Google Sheets.

- [ ] Task: Create reproduction test for inline editing and dirty state
    - [ ] Sub-task: Create `tests/gui/test_sheets_editing.py`
    - [ ] Sub-task: Write failing test that verifies `QTableWidget` is editable and "Save" button enables on edit
    - [ ] Sub-task: Run test to confirm failure (Red)

- [ ] Task: Implement Inline Editing and Dirty State
    - [ ] Sub-task: Update `mygoog_gui/pages/sheets.py` to enable editing on `QTableWidget`
    - [ ] Sub-task: Implement a signal listener for `itemChanged` to enable the "Save" button
    - [ ] Sub-task: Add "Save Changes" button to the UI
    - [ ] Sub-task: Run tests to confirm pass (Green)

- [ ] Task: Implement Save Logic (`_on_save`)
    - [ ] Sub-task: Write test for `_on_save` calling `update_range` with correct data
    - [ ] Sub-task: Implement `_on_save` method in `SheetsPage`
    - [ ] Sub-task: Connect "Save Changes" button to `_on_save`
    - [ ] Sub-task: Run tests to confirm pass (Green)

- [ ] Task: Conductor - User Manual Verification 'Update Functionality' (Protocol in workflow.md)

## Phase 2: Append Functionality (Add Row)
This phase adds a form to append new rows of data to the sheet.

- [ ] Task: Create reproduction test for Append Row form
    - [ ] Sub-task: Write failing test in `tests/gui/test_sheets_editing.py` that verifies the existence of the append form and its fields
    - [ ] Sub-task: Run test to confirm failure (Red)

- [ ] Task: Implement Append Row UI
    - [ ] Sub-task: Add "Append Row" form section at the bottom of `SheetsPage`
    - [ ] Sub-task: Dynamically generate input fields based on column headers
    - [ ] Sub-task: Add "Add Row" button
    - [ ] Sub-task: Run tests to confirm pass (Green)

- [ ] Task: Implement Append Logic
    - [ ] Sub-task: Write test for "Add Row" button calling `append_row`
    - [ ] Sub-task: Implement logic to gather form data and call `append_row`
    - [ ] Sub-task: Run tests to confirm pass (Green)

- [ ] Task: Conductor - User Manual Verification 'Append Functionality' (Protocol in workflow.md)

## Phase 3: Polish and AI Ergonomics Compliance
This phase ensures a smooth user experience, handles potential failures gracefully, and meets AI ergonomics standards.

- [ ] Task: Implement Async Feedback and Error Handling
    - [ ] Sub-task: Ensure save/append operations use async workers and show loading indicators
    - [ ] Sub-task: Implement error dialogs for API failures using "Friendly but Direct" tone
    - [ ] Sub-task: Add success notifications upon data synchronization

- [ ] Task: Verify AI Ergonomics Compliance (per `conductor/ai_ergonomics.md`)
    - [ ] Sub-task: Run `uv run mypy mygoog_gui/pages/sheets.py` - ensure 0 errors
    - [ ] Sub-task: Run `uv run ruff check mygoog_gui/pages/sheets.py` - no linting errors
    - [ ] Sub-task: Add docstrings to all new public methods (`_on_save`, append logic)
    - [ ] Sub-task: Run `uv run python scripts/run_arch_lint.py` - verify import boundaries

- [ ] Task: Verify Project Quality Gates
    - [ ] Sub-task: Verify GUI coverage >60%
    - [ ] Sub-task: Run full test suite `uv run pytest`

- [ ] Task: Conductor - User Manual Verification 'Polish and AI Ergonomics' (Protocol in workflow.md)
