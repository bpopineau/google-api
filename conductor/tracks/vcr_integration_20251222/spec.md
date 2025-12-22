# Specification: Integration Test Recording (VHS)

## Overview
Implement an integration test recording system using `vcrpy` and `pytest-recording`. This "VHS" system will allow the `mg` project to record real Google API interactions into local YAML files ("cassettes") and replay them during subsequent test runs. This is critical for improving developer ergonomics by enabling fast, deterministic, and offline-capable testing.

## Functional Requirements
- **Integration:** Add `vcrpy` and `pytest-recording` to the development toolchain.
- **Recording Mode:** Enable easy recording of new tests using `@pytest.mark.vcr` decorators.
- **Replay Logic:** By default, tests should attempt to replay from existing cassettes. If a cassette is missing, the test should fail unless explicitly run in "record" mode.
- **Security (Sanitization):** 
    - Automatically scrub `Authorization` headers (OAuth tokens) from all recorded requests.
    - Scrub sensitive fields in request/response bodies (e.g., email addresses, specific IDs if necessary).
- **Configuration:** Centralize VCR configuration in `tests/conftest.py`.

## Non-Functional Requirements
- **Performance:** Replayed tests should execute in < 100ms (excluding PySide6 startup time for GUI tests).
- **Maintainability:** Cassettes should be stored in a structured directory (e.g., `tests/cassettes/`) named after the test modules.

## Acceptance Criteria
- [ ] `pytest-recording` is installed and configured in the environment.
- [ ] Running `pytest --record-mode=none` passes for all recorded tests without hitting the network.
- [ ] Inspecting a generated cassette file confirms that the `Authorization` header has been replaced with a placeholder.
- [ ] Documentation is added to `docs/dev/testing.md` explaining how to record and refresh cassettes.

## Out of Scope
- Recording GUI-specific interactions (only network calls made by `mygooglib` and workers are recorded).
- Performance benchmarking of the API calls themselves.
