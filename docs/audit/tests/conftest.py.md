# Audit Report: tests/conftest.py

## Purpose
- Global pytest configuration, shared fixtures, and sensitive data sanitization.

## Findings
- **Privacy Focus:** Implements a robust `vcr_config` fixture that automatically redacts `authorization` headers, API keys, and post data (client secrets, refresh tokens).
- **Advanced Sanitization:** Includes a custom `_sanitize_response` function using regex to redact email addresses and access tokens embedded within response bodies.
- **Developer Ergonomics:** Automatically ensures the `cassettes/` directory exists before test execution.

## Quality Checklist
- [x] Comprehensive VCR sanitization (Headers, Query, Post Data)
- [x] Response body redaction (Regex-based)
- [x] Automatic directory management
