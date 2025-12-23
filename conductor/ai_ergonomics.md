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

*Audit performed: 2025-12-23*

| Area | Mypy Status | Files | Notes |
|------|-------------|-------|-------|
| `mygooglib/core/` | ✅ 0 errors | 28 | Excellent type coverage |
| `mygooglib/services/` | ✅ 0 errors | (incl. above) | TypedDict schemas in place |
| `mygooglib/workflows/` | ✅ 0 errors | (incl. above) | Good coverage |
| `mygoog_cli/` | ⚠️ 10 errors | 18 | `console.py` has type issues |
| `mygoog_gui/` | ✅ 0 errors | 18 | Clean |
| Context Maps | ✅ Current | 1 | `conductor/context_map.md` up-to-date |
| Directory Manifests | ✅ Good | 14 | All major dirs have MANIFEST.md |

---

## Strategic Epics (Prioritized)

### Epic 1: Fix Console.py Type Errors 🔴 High Priority
**Goal:** Resolve the 10 mypy errors in `mygoog_cli/console.py`.
**Impact:** Achieves 100% type compliance across entire codebase.
**Effort:** Low (1-2 hours)

### Epic 2: TypedDict Expansion 🟡 Medium Priority
**Goal:** Add TypedDict schemas to remaining API response types (Calendar, Tasks, Contacts, Docs).
**Impact:** Explicit contracts for all service responses, reducing type ambiguity.
**Effort:** Medium (4-6 hours)

### Epic 3: Executable Documentation 🟡 Medium Priority
**Goal:** Add `doctest` examples to all utility functions in `mygooglib/core/`.
**Impact:** Self-verifying documentation, agents can copy-paste working examples.
**Effort:** Medium (3-4 hours)

### Epic 4: GUI State Documentation 🟢 Low Priority
**Goal:** Document state transitions and signal flows in `mygoog_gui/`.
**Impact:** Reduces logic scattering, clearer entry points for UI modifications.
**Effort:** Medium (4-5 hours)

### Epic 5: Context Window Profiling 🟢 Low Priority
**Goal:** Measure token cost for common development tasks, identify optimization targets.
**Impact:** Data-driven approach to reducing context overload.
**Effort:** Low (2-3 hours)

### Epic 6: Docstring Audit 🟢 Low Priority
**Goal:** Ensure all public functions have quality docstrings (not just one-liners).
**Impact:** Better AI understanding of function behavior and edge cases.
**Effort:** High (ongoing)

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
