# Implementation Plan - Pragmatic API Response Schemas

## Phase 1: Foundation & Gmail Retrofit
Establish the schema structure and migrate the existing Gmail implementation to set the pattern.

- [ ] Task: Create `mygooglib/services/schemas/` package
    - [ ] Create directory and empty `__init__.py`
    - [ ] Create `mygooglib/services/schemas/common.py` for shared types (if any)
- [ ] Task: Retrofit Gmail Schemas
    - [ ] Create `mygooglib/services/schemas/gmail.py`
    - [ ] Define `GmailMessage`, `GmailThread`, `GmailLabel`, `GmailDraft` (Pragmatic Subset)
    - [ ] Update `mygooglib/services/gmail.py` to use new types
    - [ ] Run `mypy` to verify
- [ ] Task: Create Base Contract Test
    - [ ] Create `tests/schemas/test_contract_base.py` with helper logic
    - [ ] Create `tests/schemas/test_gmail_contract.py`
    - [ ] Verify against existing VCR cassettes
- [ ] Task: Conductor - User Manual Verification 'Foundation & Gmail Retrofit' (Protocol in workflow.md)

## Phase 2: Core Services (Calendar & Tasks)
Implement schemas for the simpler, core productivity services.

- [ ] Task: Implement Calendar Schemas
    - [ ] Create `mygooglib/services/schemas/calendar.py`
    - [ ] Define `CalendarEvent`, `CalendarListEntry`
    - [ ] Update `mygooglib/services/calendar.py`
    - [ ] Add contract tests `tests/schemas/test_calendar_contract.py`
- [ ] Task: Implement Tasks Schemas
    - [ ] Create `mygooglib/services/schemas/tasks.py`
    - [ ] Define `Task`, `TaskList`
    - [ ] Update `mygooglib/services/tasks.py`
    - [ ] Add contract tests `tests/schemas/test_tasks_contract.py`
- [ ] Task: Conductor - User Manual Verification 'Core Services (Calendar & Tasks)' (Protocol in workflow.md)

## Phase 3: Complex Services (Contacts & Docs)
Implement schemas for services with potentially deeply nested or complex structures.

- [ ] Task: Implement Contacts Schemas
    - [ ] Create `mygooglib/services/schemas/contacts.py`
    - [ ] Define `Person`, `Connection` (Pragmatic Subset)
    - [ ] Update `mygooglib/services/contacts.py`
    - [ ] Add contract tests `tests/schemas/test_contacts_contract.py`
- [ ] Task: Implement Docs Schemas
    - [ ] Create `mygooglib/services/schemas/docs.py`
    - [ ] Define `Document` (Pragmatic Subset)
    - [ ] Update `mygooglib/services/docs.py`
    - [ ] Add contract tests `tests/schemas/test_docs_contract.py`
- [ ] Task: Conductor - User Manual Verification 'Complex Services (Contacts & Docs)' (Protocol in workflow.md)

## Phase 4: Final Polish
Ensure comprehensive coverage and clean up.

- [ ] Task: Full Suite Verification
    - [ ] Run full `mypy` check
    - [ ] Run full test suite (unit + contract)
    - [ ] Update `context_map.md` (if auto-generated, or manually) to reflect new schema locations
- [ ] Task: Conductor - User Manual Verification 'Final Polish' (Protocol in workflow.md)
