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

## 💡 Quick Notes / Brainstorming
- *Idea: "Context-Aware" Gmail replies using local project data.*
- *Idea: Desktop widgets for Google Tasks.*
- *Idea: Exporting Sheets data directly to JSON for local dev use.*