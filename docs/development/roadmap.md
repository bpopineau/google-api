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
- [x] **Drive**: Upload, download, list, sync, path resolution.
- [x] **Sheets**: Open, read, write, append, A1 conversion, batch ops.
- [x] **Docs**: Create, insert, get text, template rendering, find/replace.
- [x] **Calendar**: Add, list, update, delete events.
- [x] **Tasks**: List, add, complete tasks.
- [x] **Gmail**: Send, search, mark read, save attachments.

### Step 11-15 — Advanced & Maintenance
- [x] **Patterns**: Retries, backoff, factories.
- [x] **Cleanup**: Documentation reorganization.
- [x] **CLI**: Full Typer-based interface with rich formatting.
- [x] **v0.2+ Releases**: Health improvements, Path Resolution, Workflows.

---

## 2. Implemented Features (v0.5.0)

These features are now available:

### Data & Power User Features
- [x] **Pandas Integration**: `to_dataframe()` and `from_dataframe()` for Sheets.
- [x] **Batch Operations**: `batch_get()`, `batch_update()`, and `BatchUpdater` context manager.
- [x] **Idempotency**: SQLite store to prevent duplicate writes, with `@idempotent` decorator.

### Service Extensions
- [x] **Google People (Contacts)**: Full CRUD via `ContactsClient`.

### Ergonomics
- [x] **Drive Path Resolution**: Use paths like `"Reports/2025"` instead of IDs.
- [x] **Gmail Attachments**: `save_attachments()` for query-based attachment downloading.

### Workflows
- [x] **Cross-Service recipes**: `import_events_from_sheets()` and `sync_tasks_to_calendar()`.

---

## 3. Future Feature Ideas

These are potential enhancements for future versions:

### Planned (Next)
- [ ] **Apps Script Bridge**: Trigger Apps Script functions from Python.
- [ ] **Docs v2**: Table insertion, loop/list rendering for templates.
- [ ] **Retry Tests**: Unit tests for `mygooglib/utils/retry.py`.

### Ideas (Backlog)
- [ ] **Recurrent Tasks**: Triggering workflows based on calendar events or schedules.
- [ ] **Batch Email Send**: Send multiple emails efficiently.
- [ ] **Sheets Formulas**: Helper to build complex formulas programmatically.
- [ ] **Dashboard**: Streamlit-based web UI (v0.4 scaffolding exists).

---

## 4. Version History

| Version | Date | Highlights |
|---------|------|------------|
| 0.5.0 | 2025-12-19 | BatchUpdater context manager, Gmail save_attachments |
| 0.4.0 | 2025-12-18 | Contacts CRUD, Sheets batch ops, Gmail idempotency |
| 0.3.0 | 2025-12-18 | Pandas integration, IdempotencyStore, ContactsClient |
| 0.2.0 | 2025-12-18 | Path resolution, Sheets→Calendar workflow, find/replace |
| 0.1.0 | 2025-12-17 | Initial release with core services |

See [CHANGELOG.md](../../CHANGELOG.md) for full details.
