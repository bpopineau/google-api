# Audit Report: mygooglib/core/utils/retry.py

## Purpose
- Provides robust retry logic for Google API requests, handling transient HTTP errors (429, 5xx) with exponential backoff and jitter. Distinguishes between read and write operations to prevent non-idempotent write side effects.

## Main Exports
- `execute_with_retry_http_error(...)`: Executes an API request with configurable retry parameters.
- `api_call(...)`: Decorator that wraps service methods with both retry logic and library-specific error handling.

## Findings
- **Configuration:** Deeply integrated with environment variables for fine-tuning (`MYGOOGLIB_RETRY_*`).
- **Safety:** Defaults to 1 attempt for writes (`is_write=True`), minimizing the risk of duplicate operations on network timeouts.
- **Header Support:** Correctly parses and respects `Retry-After` headers from API responses.
- **Jitter:** Applies a random jitter factor (0.85-1.15) to prevent thundering herd problems.

## TODOs
- [ ] [Technical Debt] Consider moving the `HttpError` logic into a generic retry wrapper that can handle other exception types (e.g., `socket.timeout`).
- [ ] [Feature] Implement a "budgeted" retry system to prevent a single failing operation from exhausting all retries in a tight loop.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
