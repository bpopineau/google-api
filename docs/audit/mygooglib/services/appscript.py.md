# Audit Report: mygooglib/services/appscript.py

## Purpose
- Wrapper for the Google Apps Script API, allowing Python scripts to execute functions in deployed Apps Script projects. This enables combining local Python logic with Apps Script's powerful workspace-side capabilities.

## Main Exports
- `run_function(...)`: Base implementation for script execution.
- `AppScriptClient`: Class wrapper that simplifies calling `run_function` with a pre-configured service object.

## Findings
- **Robustness:** Distinguishes between API-level errors (e.g., Auth failures) and Script execution errors (e.g., JavaScript crashes).
- **Diagnostics:** Extracts and formats script stack traces, providing crucial context for debugging remote JavaScript logic.
- **Safety:** Uses `execute_with_retry_http_error(..., is_write=True)`, which is appropriate given that Apps Script functions can produce side effects.

## TODOs
- [ ] [Feature] Consider adding a way to retrieve script metadata (e.g., list functions or deployments) to improve the client surface.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
