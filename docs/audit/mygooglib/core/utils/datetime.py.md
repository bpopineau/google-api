# Audit Report: mygooglib/core/utils/datetime.py

## Purpose
- Handles RFC3339 datetime formatting and parsing, specifically tailored for Google Calendar and Tasks APIs. Manages timezone localization with a robust fallback mechanism for environments lacking IANA timezone data (e.g., some Windows base installs).

## Main Exports
- `DEFAULT_TZ`: Global `ZoneInfo` object with `America/New_York` default and UTC fallback.
- `to_rfc3339(...)`: Converts Python date/datetime objects to ISO-8601 strings.
- `from_rfc3339(...)`: Parses ISO-8601 strings back to Python objects.

## Findings
- **Windows Robustness:** Proactively handles `ZoneInfoNotFoundError` by warning the user and falling back to UTC, which is critical for consistent behavior across OSs.
- **Normalization:** Automatically localizes naive datetimes to the default timezone, preventing accidental UTC-offset-zero assumptions.
- **RFC3339 Compliance:** Handles both all-day (date-only) and timed responses correctly.

## TODOs
- [ ] [Feature] Consider adding a utility to parse Google's slightly varied "all-day" event response formats if more edge cases are found.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
