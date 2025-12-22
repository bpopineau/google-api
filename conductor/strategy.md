# Project Strategy: The "MyGoog" Game Plan

This document outlines the high-level strategic pillars that guide the development of the `mg` project. It bridges the gap between the Product Vision (`product.md`) and the Technical Implementation (`tech-stack.md`).

## 1. The "Thick Library" Architecture
**Principle:** `mygooglib` is the single source of truth for all business logic. The GUI (`mgui`) and CLI (`mg`) are thin presentation layers.
*   **Why:** Ensures every feature is automatable and scriptable. If it works in the GUI, it must work in a Python script.
*   **Rule:** Complex workflows (e.g., "Find file, read it, email summary") belong in `mygooglib.workflows`, not in UI event handlers.
*   **Reference:** See `docs/reference/design_principles.md` (Step 12).

## 2. "Speed First" User Experience
**Principle:** The desktop app must feel instant, masking the latency of Cloud APIs.
*   **Why:** To prevent the "spinning wheel" fatigue common in web wrappers and build trust in the tool.
*   **Tactics:**
    *   **Optimistic UI:** Immediately reflect actions (e.g., "File Deleted") in the UI while the API call completes in the background. Handle errors via rollback or unobtrusive alerts.
    *   **Aggressive Caching:** Store file lists, calendar events, and contacts locally (e.g., JSON/SQLite) to enable instant app startup and "Offline Mode." Sync differences in the background.

## 3. The "Cross-Service" Value Proposition
**Principle:** Focus development on features that combine multiple Google services.
*   **Why:** This is our competitive advantage. The web UIs are siloed (Tabs); `mg` is unified.
*   **Focus Areas:**
    *   *Sheets ↔ Gmail:* "Email this range."
    *   *Drive ↔ Calendar:* "Attach file to next meeting."
    *   *Tasks ↔ Docs:* "Convert agenda to tasks."

## 4. Stability through "Strict Boundaries"
**Principle:** Decouple the Library from the Presentation layers to maintain velocity.
*   **Why:** Prevents GUI refactors from breaking CLI automation, and vice-versa.
*   **Rule:** Enforce strict TDD at the boundary.
    *   **Library:** Test pure logic with API mocking (simulating rate limits/network failures).
    *   **GUI:** Test Signals/Slots and Model updates, mocking the Library calls.

## 5. AI Ergonomics & Developer Experience
**Principle:** The codebase must be self-documenting and machine-verifiable to maximize AI agent effectiveness.
*   **Roadmap:** See [conductor/ai_ergonomics.md](./ai_ergonomics.md) for the detailed prioritized list.
*   **Tactics:**
    *   **Context Map:** Maintain an auto-generated map (`conductor/context_map.md`) of the public API surface. Agents read this first.
    *   **Strict Typing:** Enforce `disallow_untyped_defs` in `mygooglib` to provide explicit contracts.
    *   **Executable Specs:** Prefer `doctest` examples in utility functions. If an example exists in a docstring, it *must* be runnable.

