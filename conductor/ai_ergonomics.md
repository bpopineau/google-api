# AI Ergonomics Roadmap

> Making the `mg` codebase optimally readable and modifiable by AI agents.

## Vision

This document outlines the strategic roadmap for reducing "AI Friction" — the cognitive overhead an AI agent experiences when navigating, understanding, and modifying this codebase. By investing in AI ergonomics, we aim to maximize the effectiveness of AI-assisted development, enabling faster iteration cycles and higher-quality code generation.

## Philosophy: The "Zero Ambiguity" Principle

An AI-Ready codebase minimizes the number of tokens an agent must consume to understand the *intent* and *contract* of any given piece of code. This is achieved through:

1.  **Explicit Contracts:** Every function signature must fully describe its inputs and outputs via type hints and docstrings.
2.  **Predictable Structure:** Code organization follows strict conventions, allowing agents to reliably locate components without exhaustive search.
3.  **Self-Documenting Artifacts:** Manifests and context maps provide high-level summaries, reducing the need to parse raw source code for orientation.
4.  **Machine-Verifiable Rules:** Standards are enforced by automated linters to prevent ergonomic drift.

---

## AI Friction Categories

| Category | Description | Impact |
|----------|-------------|--------|
| **Context Overload** | Agent must load too many files to understand a single concept. | High token cost, inaccurate responses. |
| **Type Ambiguity** | Functions lack type hints, forcing agents to infer contracts. | Incorrect code generation, missed edge cases. |
| **Structural Inconsistency** | Similar components (services, CLI commands) follow different patterns. | Agent applies wrong pattern, causing errors. |
| **Logic Scattering** | Business logic is spread across layers (GUI, CLI, library). | Incomplete fixes, duplicated logic. |
| **Documentation Rot** | Docs/comments are outdated or contradict the code. | Agent trusts incorrect information. |

---

## Definition of AI-Done

A module is considered "AI-Ready" when it meets ALL of the following criteria:

- [ ] **100% Type Hint Coverage:** All public functions have full type annotations (parameters + return).
- [ ] **Complete Docstrings:** All public functions have a one-liner summary at minimum.
- [ ] **Manifest Present:** The containing directory has a `MANIFEST.md` or is covered by a parent manifest.
- [ ] **Context Map Entry:** The module's public API is reflected in `conductor/context_map.md`.
- [ ] **Architecture Linter Passing:** No violations from `import-linter` rules.
- [ ] **Mypy Strict Compliance:** Module passes `mypy --strict`.

---

## Current State Summary

*(To be populated by Phase 2 Audit)*

| Area | Status | Notes |
|------|--------|-------|
| `mygooglib/core/` | 🔵 Audited | Needs minor docstring improvements |
| `mygooglib/services/` | 🔵 Audited | TypedDict schemas added |
| `mygooglib/workflows/` | 🔵 Audited | Good coverage |
| `mygoog_cli/` | 🔵 Audited | Consistent Typer patterns |
| `mygoog_gui/` | 🟡 Needs Review | Complex UI state logic |
| Context Maps | 🟢 Current | Auto-generated and up-to-date |
| Directory Manifests | 🟡 Partial | Some directories lack manifests |

---

## Strategic Epics

*(To be prioritized in Phase 3)*

### Epic 1: Complete Directory Manifest Coverage
**Goal:** Every major directory has a `MANIFEST.md` summarizing its purpose, key files, and dependencies.

### Epic 2: TypedDict Expansion
**Goal:** Extend TypedDict schemas to all API response types across all services.

### Epic 3: GUI State Management Refactor
**Goal:** Centralize and document UI state transitions to reduce logic scattering.

### Epic 4: Context Window Optimization
**Goal:** Identify and refactor modules that require excessive file loading for simple tasks.

### Epic 5: Executable Documentation
**Goal:** Add `doctest` examples to all utility functions and ensure they're run in CI.

---

## Enforcement & Tooling

| Standard | Tool | Status |
|----------|------|--------|
| Type Hints | `mypy --strict` | ✅ Active |
| Import Boundaries | `import-linter` | ✅ Active |
| Code Style | `ruff` | ✅ Active |
| Context Map Generation | `scripts/generate_context_map.py` | ✅ Active |
| Manifest Validation | `scripts/run_arch_lint.py` | ✅ Active |

---

## References

- [Product Vision](./product.md)
- [Strategy](./strategy.md)
- [Context Map](./context_map.md)
- [Workflow Guidelines](./workflow.md)
- [Tech Stack](./tech-stack.md)
