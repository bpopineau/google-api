# Project Roadmap & Tracks

## Proposed Tracks

### Track 2: Gmail Attachments
**Goal:** Enable attaching local files when composing emails.
**Reference:** W6 — "Send a clean email + attachments"

- [ ] **UI:** Add "📎 Attach File" button to `ComposeDialog`
- [ ] **UI:** Display selected attachments
- [ ] **Logic:** Pass `attachments` list to `send_email`
- [ ] **Files:** `mygoog_gui/pages/gmail.py`

### Track 3: Google Docs Interface
**Goal:** Create UI for template generation and PDF export.
**Reference:** W3 — "Generate a doc from data"

- [ ] **UI:** Create `DocsPage` and add to Sidebar
- [ ] **Feature:** Template Generator (ID + Key/Value inputs)
- [ ] **Feature:** PDF Export (Context menu in Drive tree)
- [ ] **Files:** `mygoog_gui/pages/docs.py`, `mygoog_gui/widgets/sidebar.py`

---

## Future Backlog

### Gmail
- [ ] Expose bulk attachment download/save
- [ ] Add attachment preview

### Drive
- [ ] Export Docs/Sheets to `.docx`/`.xlsx`
- [ ] Add "Open in Browser" context action