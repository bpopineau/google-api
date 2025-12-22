# Project Roadmap & Tracks

## Active Tracks

### Reliability First (Offline & Error Handling)
**Goal:** Elevate error handling and offline caching to ensure dependability.
**Source:** High-level Assessment

- [ ] **UI:** Implement dedicated key-press/action error dialogs
- [ ] **Logic:** Basic offline cache for Drive/Gmail listings
- [ ] **Logic:** "Retry" mechanism for failed API calls (connectivity resilience)
- [ ] **Files:** `mygooglib/utils/errors.py`, `mygoog_gui/main.py`

### Automation Workflows (Templates)
**Goal:** Surface ready-to-run automation templates in GUI and CLI.
**Source:** High-level Assessment

- [ ] **Feature:** "Backup Local Folder to Drive" template
- [ ] **Feature:** "Sync Sheet -> Calendar" template
- [ ] **UI:** "Automations" tab in GUI to trigger these workflows
- [ ] **CLI:** `mg workflow run <template_name>` command

### Google Docs Interface
**Goal:** Create UI for template generation and PDF export.
**Reference:** W3 — "Generate a doc from data"

- [ ] **UI:** Create `DocsPage` and navigate there from Sidebar
- [ ] **Feature:** Template Generator (ID + Key/Value inputs)
- [ ] **Feature:** PDF Export
- [ ] **Files:** `mygoog_gui/pages/docs.py`

---

## Future Backlog

### Proactive Productivity
- [ ] System tray icon / background agent
- [ ] Notification layer (meetings, new emails)

### Trust & Onboarding
- [ ] First-run checklist (credentials, sync status)
- [ ] In-app recovery steps/troubleshooting

### Gmail
- [ ] Attachment support in Compose
- [ ] Bulk attachment download

### Drive
- [ ] Export Docs to common formats