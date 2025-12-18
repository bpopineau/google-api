# Roadmap & Feature Ideas

This document tracks the progress of `mygooglib` and outlines future development goals.

## 1. Project Progress (from TODO.md)

### Step 1 — Goals
- [x] Capturing v0.1 decisions.
- [x] Identifying personal automation goals.

### Step 2 — Credentials
- [x] OAuth flow implementation and token refresh verification.
- [x] Secure secret storage and `.gitignore` setup.

### Step 3 — Structure
- [x] Package layout and module organization.
- [x] Auth and utility modules.

### Step 4 — Clients
- [x] Factory for client creation.
- [x] Ergonomic class-based wrappers.

### Step 5-10 — Service Wrappers (v0.1)
- [x] **Drive**: Upload, download, list, sync.
- [x] **Sheets**: Open, read, write, append, A1 conversion.
- [x] **Docs**: Create, insert, get text, template rendering.
- [x] **Calendar**: Add, list, update, delete events.
- [x] **Tasks**: List, add, complete tasks.
- [x] **Gmail**: Send, search, mark read, attachments.

### Step 11-15 — Advanced & Maintenance
- [x] **Patterns**: Retries, backoff, factories.
- [x] **Cleanup**: Documentation reorganization (In Progress).
- [x] **CLI**: Full Typer-based interface with rich formatting.

---

## 2. New Feature Ideas

These are potential enhancements for future versions:

### Data & Power User Features
- **Pandas Integration**: `to_dataframe()` and `from_dataframe()` for Sheets.
- **Batch Operations**: Context managers for efficient bulk updates in Sheets.
- **Idempotency**: Local SQLite store to prevent duplicate writes (emails, rows).

### Service Extensions
- **Google People (Contacts)**: Add `contacts.py` for People API support.
- **Apps Script Bridge**: Trigger Apps Script functions from Python.
- **Docs v2**: Loops, tables, and rich template rendering.

### Ergonomics
- **Drive Path Resolution**: Use paths like `"Reports/2025"` instead of IDs.
- **Automated Gmail Attachments**: High-level query-based attachment saving.

### Workflows
- **Cross-Service recipes**: High-level multi-service integrations (e.g., `sync_tasks_to_calendar`).
