# Audit Report: mygoog_gui/pages/home.py

## Purpose
- The primary dashboard and overview page for the GUI.

## Main Exports
- `HomePage`: A scrollable area containing stat cards, upcoming events, pending tasks, and global search functionality.

## Findings
- **Asynchronous Loading:** Excellent use of `ApiWorker` and local functions (`fetch`) to load data from multiple services without blocking the main UI thread.
- **Global Search:** Successfully integrates the `global_search` workflow, providing a unified search across Drive and Gmail with normalized results displayed in `ItemCard`s.
- **UI Architecture:** Employs a `QStackedWidget` to seamlessly switch between the Dashboard view and Search Results view.
- **Robustness:** Handles API errors gracefully by updating stat cards with a "!" indicator and logging the failure.

## Quality Checklist
- [x] Responsive async data loading
- [x] Functional global search integration
- [x] Clear visualization with stat cards and item lists
