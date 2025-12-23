# Audit Report: mygoog_cli/workflows.py

## Purpose
- Provides CLI commands for executing high-level, cross-service workflows. It acts as the interactive interface for the "recipes" defined in `mygooglib.workflows`.

## Main Exports
- `sheets-to-calendar`: Orchestrates the transfer of event data from a spreadsheet into a Google Calendar.

## Findings
- **Integration:** Successfully bridges the CLI layer with multi-service library workflows, demonstrating how heterogeneous data (Sheets) can be transformed into actionable events (Calendar).
- **Heuristic Support:** Implements a sensible title-to-ID resolution for spreadsheets at the command level, improving user experience for those who don't have the long spreadsheet ID readily available.
- **Dry Run Support:** Correctly exposes the `dry_run` flag, providing users with a safe way to preview potentially large-scale imports before execution.

## Quality Checklist
- [x] Correctly calls library workflows
- [x] Implements title-to-ID heuristics for better UX
- [x] Provides clear summary and error reporting
