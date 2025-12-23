# Audit Report: mygooglib/services/gmail.py

## Purpose
- Wrapper for the Gmail API (v1). Provides methods for sending emails (including attachments and idempotency), searching messages with optimized metadata fetching, and managing attachments.

## Main Exports
- `send_email(...)`: Sends plain-text emails. Supports file attachments and optional idempotency keys.
- `search_messages(...)`: Searches for messages and returns lightweight metadata. Uses batch requests for performance.
- `get_message(...)` / `get_attachment(...)`: Retrieves full message content and binary attachments.
- `save_attachments(...)`: High-level utility to bulk-download attachments matching a query.
- `GmailClient`: Class wrapper for the above functions.

## Findings
- **Optimization:** `search_messages` correctly uses `new_batch_http_request()` to fetch headers for multiple messages in a single round-trip, which is crucial for performance.
- **Reliability:** `send_email` integrates with `IdempotencyStore` to prevent duplicate sends when keys are provided.
- **Complexity Management:** Body extraction in `get_message` handles nested MIME parts (walking the payload tree), which is necessary for modern HTML/Multipart emails.
- **Safety:** `save_attachments` handles duplicate filenames by appending a message ID prefix, preventing accidental overwrites.

## TODOs
- [ ] [Feature] Add support for HTML email bodies in `send_email`. Currently, it only supports plain text.
- [ ] [Technical Debt] The batch request wrapper `_BatchWrapper` is a bit of a hack to work with `execute_with_retry_http_error`. We should consider making the retry helper natively support batch requests.

## Quality Checklist
- [x] Docstrings follow project style
- [x] Type hints are complete and modern
- [x] Unused code removed
- [x] Logically verified for edge cases
