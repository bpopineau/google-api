# Track Specification: Re-establish AI Ergonomics Roadmap

## 1. Overview
The goal of this track is to re-establish and formalize the "AI Ergonomics Roadmap" for the `mg` project. This involves restoring the strategic vision for making the codebase easier for AI agents to navigate, understand, and modify. The track will combine restoring lost context, conducting a fresh audit of the current codebase state, and defining new standards to reduce "friction" (context overload, ambiguity, inconsistency) for future AI interactions.

## 2. Functional Requirements

### 2.1 Restoration & Definition
-   [ ] Restore/Create `conductor/ai_ergonomics.md` as the central source of truth for AI-specific improvements.
-   [ ] Define clear categories of "AI Friction" (e.g., Context Overload, Type Ambiguity, Structural Inconsistency).

### 2.2 Codebase Audit
-   [ ] Conduct a high-level audit of the current codebase to identify:
    -   Modules with poor type coverage.
    -   Directories lacking clear "manifests" or high-level documentation.
    -   Inconsistent patterns in UI (PySide6) or CLI logic.
-   [ ] Document these findings directly in the roadmap as prioritized "Epics" or "Tasks".

### 2.3 Standard Setting
-   [ ] Define specific "AI-Friendly" standards (e.g., "All major directories must have a `MANIFEST.md`").
-   [ ] Update `conductor/product-guidelines.md` or create `conductor/code_styleguides/ai_standards.md` if necessary to formalize these rules.

### 2.4 Artifact Generation
-   [ ] Generate or update "Context Maps" (e.g., `conductor/context_map.md`) if they are outdated or missing, to prove the value of the new roadmap.
-   [ ] Identify and list specific tooling improvements (like new linter rules) that would enforce these standards automatically.

## 3. Non-Functional Requirements
-   **Documentation Quality:** The roadmap itself must be concise and optimized for AI reading (high information density, clear structure).
-   **Actionable:** Every item on the roadmap must be actionable (convertible into a future Track).

## 4. Acceptance Criteria
-   [ ] `conductor/ai_ergonomics.md` exists and contains a prioritized list of at least 5 major improvement areas.
-   [ ] An initial audit has been performed, and its results are summarized in the roadmap.
-   [ ] A "Context Map" or similar high-level summary of the codebase is up-to-date and referenced.
-   [ ] A standard for "AI-Ready" code (typing, docstrings, manifests) is documented.

## 5. Out of Scope
-   Implementing all the specific refactoring tasks identified in the roadmap (this track is about *identifying* and *planning* them, not doing them all).
-   Major architectural rewrites (unless identified as a roadmap item for later).