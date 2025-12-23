# Audit Report: scripts/generate_context_map.py

## Purpose
- Auto-generates `conductor/context_map.md` by introspecting the `mygooglib` public API surface.

## Findings
- **Powerful Introspection:** Uses `pkgutil` and `inspect` to dynamically discover service clients and their public methods.
- **AI-Friendly:** The generated output is specifically formatted to provide a concise "context map" for AI agents to understand available tools.
- **Robustness:** Includes basic error handling for ImportErrors and signature extract failures.

## Quality Checklist
- [x] Successfully introspects service clients
- [x] Generates AI-optimized documentation
