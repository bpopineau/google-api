# tests

## Purpose
The automated test suite for ensuring code correctness and preventing regressions. It covers unit tests, integration tests, and GUI tests using `pytest`.

## Key Entry Points
- [`conftest.py`](file:///c:/Users/brand/Projects/google-api/tests/conftest.py): Global test configuration, fixtures (e.g., `mock_auth`, `vcr_config`), and plugins.
- [`test_auth.py`](file:///c:/Users/brand/Projects/google-api/tests/test_auth.py): Verifies authentication logic.
- [`test_gmail_attachments.py`](file:///c:/Users/brand/Projects/google-api/tests/test_gmail_attachments.py): Example of service-specific integration tests.

## Dependencies
- **External:** `pytest`, `pytest-qt`, `vcrpy`, `pytest-cov`
- **Internal:** `mygooglib` (the code under test)
