# Roadmap & Feature Ideas

This document tracks the progress of `mygooglib` and outlines future development goals.

## 1. Project Progress

### Core Foundation
- [x] OAuth flow and token refresh
- [x] Package layout and module organization
- [x] Factory for client creation with lazy loading
- [x] Ergonomic class-based wrappers

### Service Wrappers
- [x] **Drive**: Upload, download, list, sync, path resolution
- [x] **Sheets**: Read, write, append, batch ops, Pandas integration
- [x] **Docs**: Create, template rendering, find/replace, tables, lists
- [x] **Calendar**: Add, list, update, delete events
- [x] **Tasks**: List, add, complete tasks
- [x] **Gmail**: Send, search, mark read, save attachments
- [x] **Contacts**: List, search, create, update, delete (People API)

### Advanced Features
- [x] **Retry with Backoff**: Automatic retry on 429/5xx errors
- [x] **Idempotency Store**: SQLite-based duplicate prevention
- [x] **CLI**: Full Typer-based interface with rich formatting
- [x] **Cross-Service Workflows**: Sheets→Calendar, etc.

---

## 2. Current Version (v0.6.0)

### Recent Additions
- [x] **Docs v2**: `insert_table()` and `render_list()` for rich templates
- [x] **Retry Tests**: Comprehensive unit tests for retry module
- [x] **Examples**: New example scripts for contacts, batch ops, idempotency

### Power User Features
- [x] **Pandas Integration**: `to_dataframe()`/`from_dataframe()` for Sheets
- [x] **Batch Operations**: `batch_get()`, `batch_update()`, `BatchUpdater`
- [x] **Gmail Attachments**: Query-based attachment downloading

---

## 3. Future Feature Ideas

### Planned
- [ ] **Apps Script Bridge**: Execute Apps Script functions from Python (scaffolding complete)
- [ ] **Recurrent Tasks**: Trigger workflows based on schedules

### Backlog
- [ ] **Batch Email Send**: Send multiple emails efficiently
- [ ] **Sheets Formulas**: Helper to build complex formulas
- [ ] **Dashboard**: Streamlit-based web UI

---

## 4. Version History

| Version | Date | Highlights |
|---------|------|------------|
| 0.6.0 | 2025-12-19 | Docs v2 (tables, lists), retry tests, examples |
| 0.5.0 | 2025-12-19 | BatchUpdater, Gmail save_attachments |
| 0.4.0 | 2025-12-18 | Contacts CRUD, batch ops, Gmail idempotency |
| 0.3.0 | 2025-12-18 | Pandas integration, IdempotencyStore |
| 0.2.0 | 2025-12-18 | Path resolution, Sheets→Calendar workflow |
| 0.1.0 | 2025-12-17 | Initial release with core services |

See [CHANGELOG.md](../../CHANGELOG.md) for full details.
