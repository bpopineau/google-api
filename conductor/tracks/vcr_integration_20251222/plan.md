# Implementation Plan: Integration Test Recording (VHS)

## Phase 1: Infrastructure & Sanitization
Configure the core VCR engine to ensure secure and consistent recording.

- [x] **Task 1: Install VCR Dependencies** [c0e6f31]
    - Add `vcrpy` and `pytest-recording` to the environment (via `uv add --dev`).
    - Verify installation with `pytest --version`.
- [x] **Task 2: Configure Global VCR Sanitizers** [924bae8]
    - Update `tests/conftest.py` to include a `pytest_recording_configure` hook.
    - Implement `filter_headers` to replace 'Authorization' with `<ACCESS_TOKEN>`.
    - Implement `filter_post_data_parameters` for common sensitive fields.
- [x] **Task: Conductor - User Manual Verification 'Infrastructure & Sanitization' (Protocol in workflow.md)**

## Phase 2: Core Implementation & Verification (TDD)
Apply the system to existing tests to verify the recording and replay lifecycle.

- [x] **Task 1: Red Phase - Fail Offline Execution**
    - Annotate `tests/test_sheets_exists.py` (or similar) with `@pytest.mark.vcr`.
    - Run `pytest --record-mode=none`.
    - **Expected Result:** Test fails because no cassette exists.
- [~] **Task 2: Green Phase - Record and Replay**
    - Run `pytest --record-mode=once` to generate the cassette.
    - Run `pytest --record-mode=none` again.
    - **Expected Result:** Test passes using the local cassette.
- [ ] **Task 3: Refactor - Refine Cassette Organization**
    - Ensure cassettes are stored in `tests/cassettes/`.
    - Verify YAML content for sanitization (manually check for leaked tokens).
- [ ] **Task: Conductor - User Manual Verification 'Core Implementation & Verification' (Protocol in workflow.md)**

## Phase 3: Documentation & Standardization
Finalize the developer experience for other contributors (and future me).

- [ ] **Task 1: Create Developer Testing Guide**
    - Write `docs/dev/testing.md`.
    - Explain the recording modes (`once`, `none`, `all`, `rewrite`).
    - Document how to refresh cassettes when APIs change.
- [ ] **Task 2: Broaden Test Coverage**
    - Apply VCR recording to `tests/test_docs_features.py` and `tests/test_auth.py`.
    - Ensure CI configuration (if any) is updated to run in `none` mode.
- [ ] **Task: Conductor - User Manual Verification 'Documentation & Standardization' (Protocol in workflow.md)**
