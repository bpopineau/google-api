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

## 🛠️ Feature Tracks (Product Requirements)

### 4. Google Docs Template Engine (W3)
**Concept:** Implement `docs.render_template(template_id, mapping)` to generate documents from data and export them to PDF.
*   **AI Ergonomics:** Defines strict mappings for template variables. Uses **VCR** to record complex doc generation flows.
*   **Reference:** Requirements W3.

### 5. Proactive Productivity (Background Agent)
**Concept:** A system tray icon or background process that monitors for upcoming meetings or urgent emails.
*   **AI Ergonomics:** Leverages the **Unified Console** for background log inspection. Requires robust **Offline Caching** logic.
*   **Reference:** Strategy Pillar #2 (Speed First).

## 🧪 Experimental / Refinement

### 6. Local-to-Cloud Sync (W1 Upgrade)
**Concept:** Full two-way synchronization for the `sync_folder` feature, including conflict resolution and "safe delete" logic.
*   **AI Ergonomics:** Uses **Dry Run Reports** to explain sync conflicts to the user before they happen.
*   **Reference:** Requirements W1.

---

## 💡 Quick Notes / Brainstorming
- *Idea: "Context-Aware" Gmail replies using local project data.*
- *Idea: Desktop widgets for Google Tasks.*
- *Idea: Exporting Sheets data directly to JSON for local dev use.*
