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

### 14. 🗺️ Re-establish AI Ergonomics Roadmap
**Concept:** `conductor/ai_ergonomics.md` is missing but referenced in `strategy.md`. This track involves auditing the current "AI friendliness" and documenting the missing pieces (Context Maps, Doctests, etc.).
*   **Strategic Impact:**
    *   **Strategy:** Realigns the project with its core "AI First" philosophy.

---

## 💡 Quick Notes / Brainstorming
- *Idea: "Context-Aware" Gmail replies using local project data.*
- *Idea: Desktop widgets for Google Tasks.*
- *Idea: Exporting Sheets data directly to JSON for local dev use.*