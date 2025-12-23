# Audit Report: mygooglib/workflows/__init__.py

## Purpose
- Package initializer for `mygooglib.workflows`. Re-exports high-level workflows for easier access from the root package or application layer.

## Main Exports
- `global_search`: The multi-service search workflow.
- `import_events_from_sheets`: The Sheets-to-Calendar integration workflow.

## Findings
- **Implementation:** Correctly re-exports specialized workflows, providing a single entry point for all high-level logic.
- **Controlled Exports:** Properly uses `__all__` to restrict the public surface.

## Quality Checklist
- [x] Workflow re-exports are correct
- [x] `__all__` is accurately defined
