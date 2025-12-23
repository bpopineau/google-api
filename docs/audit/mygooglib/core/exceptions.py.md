# Audit Report: mygooglib/core/exceptions.py

## Purpose
- Defines custom exception types for the library and provides a translation utility to convert raw `googleapiclient.errors.HttpError` into actionable, domain-specific exceptions with user-friendly hints.

## Main Exports
- `GoogleApiError`: Base class for all library exceptions.
- `AuthError`, `NotFoundError`, `QuotaExceededError`, `InvalidRequestError`: Specialized exceptions for common HTTP status codes.
- `raise_for_http_error(...)`: Centralized error translation function.

## Findings
- **Actionable Hints:** Provides excellent hints for `401/403` and `429` errors, guiding users on how to resolve the issues (e.g., re-authenticating or batching).
- **Lazy Imports:** Proactively avoids module-load bloat by lazily importing `HttpError`.
- **Robustness:** Handles cases where `HttpError` might not have `_get_reason()` by falling back to `str(http_error)`.

## TODOs
- [ ] [Consistency] Audit all service implementations to ensure `raise_for_http_error` is used for every API call.
- [ ] [Feature] Add specialized exceptions for 5xx "Server Error" scenarios to distinguish between client-side and server-side issues.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
