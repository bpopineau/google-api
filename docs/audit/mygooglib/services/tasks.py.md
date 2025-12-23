# Audit Report: mygooglib/services/tasks.py

## Purpose
- Wrapper for the Google Tasks API (v1). Provides methods for managing task lists and performing CRUD operations on individual tasks, including due date and status management.

## Main Exports
- `list_tasklists(...)`: Retrieves the user's task lists.
- `add_task(...)`: Creates a new task with optional notes and due dates.
- `list_tasks(...)`: Lists tasks in a specific list. Handles pagination.
- `complete_task(...)` / `update_task(...)`: Modifies task status and properties.
- `delete_task(...)`: Permanently removes a task.
- `TasksClient`: Class wrapper for the above functions.

## Findings
- **Simplicity:** The module correctly uses `@default` as a sentinel for the primary task list, making it very easy to use for simple "todo" apps.
- **Pagination:** `list_tasks` correctly implements a `while True` loop with `nextPageToken` to collect all results, and respects the `max_results` limit.
- **Type Safety:** Uses `datetime` objects for due dates, converting them internally to RFC3339 strings via the project utility.

## TODOs
- [ ] [Technical Debt] All functions return `dict` or `list[dict]` for task data. These should be updated to use specific `TypedDict` schemas (e.g., `TaskDict`) for better Mypy support, similar to other service wrappers.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
