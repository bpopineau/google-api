# Audit Report: tests/test_global_search.py

## Purpose
- Integration tests for the Global Search functionality within the GUI.

## Findings
- **Asynchronous Logic Handling:** Correctly mocks and verifies the `global_search` workflow call from the `HomePage`.
- **Worker Simulation:** Successfully simulates the `ApiWorker` signaling mechanism to verify that search triggers the appropriate background logic.
- **UI State Verification:** Properly mocks complex UI components (QStack, QListWidget) to focus strictly on the search delegation logic.

## Quality Checklist
- [x] Verified global_search delegation
- [x] Mocked asynchronous worker execution
