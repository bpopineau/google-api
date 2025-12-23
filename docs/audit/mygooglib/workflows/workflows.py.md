# Audit Report: mygooglib/workflows/workflows.py

## Purpose
- Contains high-level, multi-service workflows that orchestrate complex operations spanning different Google APIs.

## Main Exports
- `import_events_from_sheets(...)`: Reads a range from a spreadsheet and creates corresponding events in Google Calendar. Supports duration-based or timestamp-based end times.

## Findings
- **Cross-Service Logic:** Successfully orchestrates `sheets.get_range` and `calendar.add_event`.
- **Flexibility:** The logic for interpreting the "End" column (detecting if it's an integer duration vs. a timestamp string) is practical for real-world spreadsheet data.
- **Dry Run Support:** Correctly implements `dry_run` to allow users to verify import logic without polluting their calendar.
- **Robustness:** Skips empty rows and logs errors per-row, ensuring that one bad data row doesn't abort the entire import process.

## TODOs
- [ ] [Feature] Add support for batching `add_event` calls (if supported by a batch helper) to improve performance for large imports.
- [ ] [Technical Debt] The column mapping is currently hardcoded (`row[0]`, `row[1]`, etc.). This could be improved by allowing users to pass a column map or by looking for specific header names.

## Quality Checklist
- [x] Orchestrates multiple services correctly
- [x] Handles heterogeneous data types (duration vs end time)
- [x] Implements row-level error isolation
