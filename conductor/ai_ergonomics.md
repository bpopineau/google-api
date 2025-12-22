# AI Agent Ergonomics Roadmap

This document outlines the strategy for maximizing the effectiveness of AI agents working on this repository. The goal is to make the codebase "machine-friendly"—easy to navigate, safe to experiment in, and strict in its feedback.

## 🥇 Tier 1: The "Cognitive Grounding" Layer
*Foundational tools. Without these, the agent is guessing.*

### 1. [x] Context Map (`conductor/context_map.md`)
*   **What:** Auto-generated summary of every tool, class, and method signature.
*   **Why:** Solves "Discovery". The agent sees the entire toolkit in one glance.
*   **Status:** **Implemented** (via `scripts/generate_context_map.py`).

### 2. [x] Strict Typing (TypedDicts/Schemas)
*   **What:** Convert loose `dict` returns from Google APIs into strict `TypedDict` or `Pydantic` models.
*   **Why:** Solves "Hallucination". Agents know exactly what fields exist (e.g., `mimeType` vs `mime_type`) without inspecting live API responses.
*   **Status:** **Implemented** (via `mygooglib/core/types.py`).

### 3. [x] Semantic Error Codes (Structured Exceptions)
*   **What:** Wrap opaque `HttpError` (403/404) into clean domain exceptions (`PermissionDeniedError`, `ResourceNotFoundError`).
*   **Why:** Solves "Self-Correction". Agents get clear, actionable signals ("File not found") instead of raw JSON noise.
*   **Status:** **Implemented** (via `mygooglib/core/exceptions.py`).

## 🥈 Tier 2: The "Safety & Simulation" Layer
*Tools that allow agents to act confidently without destroying data.*

### 4. [ ] Verbose "Dry Run" Simulator
*   **What:** Destructive methods (`delete`, `update`) support `dry_run=True` and return a structured JSON report.
*   **Why:** Solves "Hesitation". Agents can simulate a cleanup script, verify the targeted files in the JSON report, and then execute for real.

### 5. [x] Integration Test Recorder (VCR.py)
*   **What:** Record real API interactions into "cassettes" for offline replay.
*   **Why:** Solves "Testability". Agents can write/verify features without needing real Google credentials, enabling "Test-Driven Debugging".
*   **Status:** **Implemented** (via `tests/test_vcr_integration.py` and `tests/conftest.py`).

### 6. [ ] Deterministic Data Factories
*   **What:** Helper library (`tests/factories.py`) generating predictable mock objects.
*   **Why:** Solves "Flakiness". Agents can write tests with hardcoded assertions, knowing the input data structure is constant.

## 🥉 Tier 3: The "Navigation & Workflow" Layer
*Optimizations for agent efficiency and architectural alignment.*

### 7. [ ] Directory Manifests (`MANIFEST.md`)
*   **What:** Small readmes in subdirectories explaining their "Single Responsibility".
*   **Why:** Solves "Context Fragmentation". Agents follow a map rather than opening every file.

### 8. [ ] Task Scaffolding Scripts
*   **What:** CLI tools to generate boilerplate (e.g., `python scripts/scaffold_service.py`).
*   **Why:** Solves "Consistency". Prevents agents from inventing file structures or missing registration steps.

### 9. [ ] Architecture Linter
*   **What:** Custom lint rules banning specific imports (e.g., "GUI cannot import `googleapiclient`").
*   **Why:** Solves "Drift". Automated guardrails correcting architectural violations instantly.

### 10. [ ] Unified Debug Console (REPL)
*   **What:** Pre-configured shell environment (`mg console`).
*   **Why:** Solves "Exploration". Quick way for agents to "poke" the system and verify assumptions.
