# Project Backlog & Ideas

This file tracks potential future tracks and feature ideas. These are "promoted" to `conductor/tracks.md` when they are ready for implementation.

## 🚀 High Priority (Strategic Impact)

### 1. Declarative Workflow Engine ("The Automation Hub")
**Concept:** Implement a system to define multi-step automation rules using YAML or Python scripts (e.g., *"When a new email arrives with an invoice, save to Drive and update the 'Expenses' Sheet"*).
*   **AI Ergonomics:** Uses **Strict Schemas** to pipe data between services. Critical use case for **Dry Run Simulator** (show the "Plan of Action" before execution) and **VCR** (record trigger scenarios).
*   **Reference:** Strategy Pillar #3 (Cross-Service Value).

### 2. Unified "Omnibar" Search Interface
**Concept:** A central search bar in the GUI and a `mg search` CLI command that queries Drive, Gmail, and Tasks simultaneously.
*   **AI Ergonomics:** Requires a new `SearchResult` **Strict Schema** to normalize diverse API responses. Leverages **Data Factories** for UI stress-testing without API hits.
*   **Reference:** Strategy Pillar #3 (Unified Command Center).

### 3. "Smart Actions" CLI (Intent-Based Commands)
**Concept:** CLI commands that accept high-level intents and generate a structured "Plan" for approval. (e.g., `mg cleanup --older-than 30d --folder "Downloads"`).
*   **AI Ergonomics:** The star of the **Verbose Dry Run** system. Generates a markdown report of every file to be touched. Fully testable in the **Unified Console**.

### 4. "Smart Cache" Layer (Zero-Latency Mode)
**Concept:** Persistent local cache (SQLite or JSON) for listings. The app loads from cache *instantly* on startup, then syncs with APIs in the background.
*   **AI Ergonomics:** Relies on **Strict Schemas** for storage/retrieval consistency. Testable via **VCR** for offline/conflict scenarios. Inspectable in the **Unified Console**.
*   **Reference:** Strategy Pillar #2 (Speed First).

## 🛠️ Feature Tracks (Product Requirements)

### 5. Google Docs Template Engine (W3)
**Concept:** Implement `docs.render_template(template_id, mapping)` to generate documents from data and export them to PDF.
*   **AI Ergonomics:** Defines strict mappings for template variables. Uses **VCR** to record complex doc generation flows.
*   **Reference:** Requirements W3.

### 6. Proactive Productivity (Background Agent)
**Concept:** A system tray icon or background process that monitors for upcoming meetings or urgent emails.
*   **AI Ergonomics:** Leverages the **Unified Console** for background log inspection. Requires robust **Offline Caching** logic.
*   **Reference:** Strategy Pillar #2 (Speed First).

### 7. "Universal Clipboard" Integration
**Concept:** Auto-detect copied Google URLs or data patterns and offer immediate actions (e.g., "Open in Console", "Download as CSV").
*   **AI Ergonomics:** Logic can be refined/tested in the **Unified Console** (`mg.analyze_clipboard()`). Uses **Data Factories** to simulate diverse clipboard inputs.

### 8. "Data Lens" (Visual Data Explorer)
**Concept:** A dedicated GUI view for inspecting arbitrary Google Sheets or JSON data as a filterable, sortable table (like a lightweight Pandas viewer).
*   **AI Ergonomics:** Uses **Strict Schemas** for typed rendering. Leverages **Data Factories** for performance benchmarking.
*   **Reference:** Strategy Pillar #1 (Thick Library).

### 9. Global Keyboard Shortcuts & Command Palette
**Concept:** Implement comprehensive keyboard shortcuts across the GUI and add a VS Code-style command palette (Ctrl+Shift+P).
*   **Priority:** High - Core product guideline missing from current implementation.
*   **Features:**
    *   Global hotkeys for rapid actions (quick add task, archive email, etc.)
    *   Full keyboard navigation support across all widgets
    *   Command palette for all actions
    *   Tooltips showing keyboard shortcuts on all buttons
*   **Reference:** Product Guidelines (Keyboard Centricity).

### 10. Elevated Global Omnibar
**Concept:** Transform the home page search into a true global overlay modal (Ctrl+K) accessible from any page.
*   **Priority:** High - Product guideline emphasizes "Unified Search" as central Omnibar.
*   **Features:**
    *   Overlay modal with instant search across Drive, Gmail, Calendar, Tasks
    *   Keyboard-driven results navigation
    *   Quick actions on results (open, archive, delete)
    *   Recent searches history
*   **Reference:** Product Guidelines (Unified Search) + Strategy Pillar #3.

### 11. GUI Visual Polish & Professional Icons
**Concept:** Replace emoji icons with professional icon set and enhance visual hierarchy with modern design patterns.
*   **Priority:** Medium - Improves "Polished Feel" from product guidelines.
*   **Features:**
    *   Replace emoji with Material Icons or Phosphor icon set
    *   Add subtle shadows, depth cues to cards
    *   Implement smooth page transitions (QPropertyAnimation)
    *   Add micro-interactions (hover effects, loading states)
    *   Compact sidebar mode (icon-only toggle)
*   **Reference:** Product Guidelines (Polished Feel, Modern Dark Mode).

### 12. Split View & Enhanced Activity Feedback
**Concept:** Implement split-view capability and enhanced activity widget for background tasks.
*   **Priority:** Medium - Product guideline feature gap.
*   **Features:**
    *   Split views for simultaneous contexts (Task list + Calendar)
    *   Enhanced activity widget with real-time automation feedback
    *   Status bar at bottom for background task progress
    *   Console feedback panel for automation task logs
*   **Reference:** Product Guidelines (Split Views, Console Feedback).

### 13. Quick Capture Panel (Floating Mini-Interface)
**Concept:** Global hotkey-activated floating panel for rapid task/email/event creation without switching to the full app.
*   **Priority:** High - Maximum impact/effort ratio for keyboard-centric users.
*   **Features:**
    *   Global hotkey (e.g., `Ctrl+Shift+N`) to summon floating panel
    *   Quick task creator with minimal fields
    *   "Save to Drive" for clipboard URLs/files
    *   Email draft starter
    *   Event quick-add with natural language parsing
    *   Always-on-top, compact UI
*   **Impact:** Massive friction reduction for power users during flow state.
*   **Reference:** Product Guidelines (Keyboard Centricity, Efficiency).

### 14. "Today View" - Contextual Daily Dashboard
**Concept:** Single-pane daily execution dashboard combining calendar, tasks, and priority emails.
*   **Priority:** High - Addresses "Unified Command Center" vision.
*   **Features:**
    *   Morning agenda: Next 3 calendar events with one-click join links
    *   Today's task list with drag-to-reorder priority
    *   Unread priority emails (starred/important)
    *   Quick stats dashboard: meetings remaining, tasks completed, emails processed
    *   Time-aware: adapts throughout the day
*   **Impact:** Single pane of glass for daily execution, reduces context switching.
*   **Reference:** Strategy Pillar #3 (Unified Command Center).

### 15. Drag-and-Drop Cross-Service Actions
**Concept:** Universal drag-and-drop for moving information between Google services.
*   **Priority:** High - Natural, visual workflow shortcuts.
*   **Features:**
    *   Drag Gmail message → Tasks = "Create task from email"
    *   Drag Drive file → Gmail = "Attach to draft"
    *   Drag Calendar event → Drive = "Create meeting notes doc"
    *   Drag Task → Calendar = "Schedule time to work on this"
    *   Visual feedback during drag operations
*   **Impact:** Intuitive cross-service workflows, demonstrates "Cross-Service Value".
*   **Reference:** Strategy Pillar #3 (Cross-Service Value).

### 16. Smart Context Sidebar (Dynamic "What's Relevant Now")
**Concept:** Transform activity widget into context-aware assistant showing actionable information.
*   **Priority:** Medium - Enhances existing right sidebar with intelligence.
*   **Features:**
    *   During calendar events: Show event details, attendees, related files from Drive
    *   When viewing emails: Show related threads, calendar events with sender
    *   When on Tasks page: Show available calendar slots to schedule work
    *   "Pending actions" section: unanswered emails, overdue tasks, upcoming deadlines
    *   Context changes based on current page and time of day
*   **Impact:** Reduces cognitive load and tab-switching.
*   **Reference:** Product Guidelines (Functional Density).

### 17. Batch Operations Toolbar
**Concept:** Multi-select mode with keyboard-driven batch actions across all services.
*   **Priority:** Medium - 10x efficiency for power users.
*   **Features:**
    *   Multi-select mode (checkbox UI + keyboard shortcuts)
    *   Batch actions: Archive all, Label all, Move all, Share with team
    *   Keyboard shortcuts: select-all (`Ctrl+A`), select-by-filter, invert selection
    *   Undo history for batch operations with visual confirmation
    *   Works across Gmail, Drive, Tasks
*   **Impact:** Massive efficiency gain for bulk email/file processing.
*   **Reference:** Product Guidelines (Keyboard Centricity, Efficiency).

### 18. "Focus Mode" with Do Not Disturb
**Concept:** Toggle mode that silences live updates and distractions to support deep work.
*   **Priority:** Low - Nice-to-have for concentration.
*   **Features:**
    *   Pauses activity feed updates and notifications
    *   Hides unread counts/badges from all tabs
    *   Optional: Auto-reply to emails during focus blocks
    *   Pomodoro timer integration (25min work, 5min break)
    *   Keyboard shortcut to toggle (`Ctrl+Shift+F`)
    *   Restoration of state when exiting focus mode
*   **Impact:** Supports deep work habits for knowledge workers.
*   **Reference:** Product Guidelines (Polished Feel).

### 19. Universal "Link Anything" System (Internal URI Scheme)
**Concept:** Internal `mygoog://` URI scheme for linking between items across services.
*   **Priority:** Medium - Power-user feature for building "second brain".
*   **Features:**
    *   Right-click any item → "Copy MyGoog Link"
    *   Generates shareable internal URIs (e.g., `mygoog://task/abc123`)
    *   Paste into notes, task descriptions, calendar event details
    *   Links open directly in the app to that specific item
    *   Works for Drive files, emails, tasks, calendar events, sheets
    *   Enables building interconnected knowledge graphs
*   **Impact:** Powerful for knowledge workers who build reference systems.
*   **Reference:** Strategy Pillar #3 (Cross-Service Value).

### 20. Template & Snippet Library
**Concept:** Built-in templates system for recurring email replies, task structures, and event descriptions.
*   **Priority:** Low - Reduces repetitive typing.
*   **Features:**
    *   Email templates with variable substitution (e.g., "Meeting Follow-up")
    *   Task list templates (e.g., "New Project Setup Checklist")
    *   Calendar event templates with pre-filled details and attendees
    *   Accessible via command palette or dedicated hotkey
    *   Import/export templates for sharing with team
*   **Impact:** Time savings on routine communications.
*   **Reference:** Product Guidelines (Efficiency).

### 21. Timeline View (Unified Activity Stream)
**Concept:** Chronological timeline showing all activity across services for retrospectives.
*   **Priority:** Low - Great for time tracking and accountability.
*   **Features:**
    *   Unified chronological stream: emails sent/received, files uploaded, events attended, tasks completed
    *   Filterable by service type and date range
    *   Search within timeline
    *   Export to CSV for time tracking
    *   Useful for daily reviews and retrospectives
*   **Impact:** Visibility into "what happened today" across all services.
*   **Reference:** Strategy Pillar #3 (Unified Command Center).

### 22. Mini-Map Navigation (Spatial File Browser)
**Concept:** Visual folder tree sidebar for Drive navigation (VS Code-style file explorer).
*   **Priority:** Medium - Essential for Drive power users.
*   **Features:**
    *   Collapsible folder tree structure in left panel
    *   Drag files between folders in the tree view
    *   Breadcrumb navigation at top of content area
    *   Keyboard navigation: arrow keys to traverse tree, Enter to open
    *   "Starred" and "Recent" smart folders at top
    *   Right-click context menu for folder operations
*   **Impact:** Eliminates clicking through deep folder hierarchies.
*   **Reference:** Product Guidelines (Functional Density, Keyboard Centricity).

## 🧪 Experimental / Refinement

### 9. Local-to-Cloud Sync (W1 Upgrade)
**Concept:** Full two-way synchronization for the `sync_folder` feature, including conflict resolution and "safe delete" logic.
*   **AI Ergonomics:** Uses **Dry Run Reports** to explain sync conflicts to the user before they happen.
*   **Reference:** Requirements W1.

---

## 🧠 Brainstormed Strategic Tracks

### 10. 👻 Ghost Mode (Offline Data Factories)
**Concept:** A dedicated `mg --ghost` mode that disconnects all APIs and serves high-fidelity fake data (via `faker`) for Drive, Gmail, Sheets, etc.
*   **Strategic Impact:**
    *   **Speed First:** Enables creating/testing complex workflows on an airplane.
    *   **AI Ergonomics:** Allows AI agents to write & run code fearlessly without risk of deleting real files or emailing the CEO.
    *   **Reference:** Promotes the "Data Factories" concept to a core architecture pillar.

### 11. 🔐 Unified Identity & Session Manager
**Concept:** A robust `AuthManager` that handles multiple Google accounts (Personal vs Work), incremental scope upgrades, and background token refreshing.
*   **Strategic Impact:**
    *   **Foundation:** Essential for the "Unified Command Center" vision.
    *   **UX:** Solves the "re-login" friction.
    *   **Security:** "Least privilege" by requesting scopes only when needed.

### 12. 🧠 "Smart Context" Service (Local RAG)
**Concept:** A background service that indexes `conductor/`, `docs/`, and local data to provide a semantic search API (`mg.ask("how do I add a new track?")`).
*   **Strategic Impact:**
    *   **AI Ergonomics:** The ultimate "Self-Documenting" feature.
    *   **Automation Hub:** Enables "Natural Language to Workflow" features later.

### 13. 📜 Activity Journal (The "Black Box")
**Concept:** A structured, immutable log (SQLite/JSONL) of every "write" action taken by `mygooglib`.
*   **Strategic Impact:**
    *   **Trust:** Critical for an "Automation Hub". User needs to know *exactly* what the script deleted.
    *   **Refinement:** "Undo" functionality becomes possible if we have the diffs.

### 14. ~~Re-establish AI Ergonomics Roadmap~~ ✅ COMPLETE
**Status:** Implemented in track `ai_ergonomics_20251223`. See `conductor/ai_ergonomics.md`.

### 15. 🔴 Fix Console.py Type Errors (AI Ergonomics Epic 1)
**Concept:** Resolve 10 mypy errors in `mygoog_cli/console.py` to achieve 100% type compliance.
*   **Effort:** Low (1-2 hours)
*   **Reference:** AI Ergonomics Roadmap Epic 1.

### 16. 🟡 TypedDict Expansion (AI Ergonomics Epic 2)
**Concept:** Add TypedDict schemas to Calendar, Tasks, Contacts, and Docs API responses.
*   **Effort:** Medium (4-6 hours)
*   **Reference:** AI Ergonomics Roadmap Epic 2.

---

## 💡 Quick Notes / Brainstorming
- *Idea: "Context-Aware" Gmail replies using local project data.*
- *Idea: Desktop widgets for Google Tasks.*
- *Idea: Exporting Sheets data directly to JSON for local dev use.*