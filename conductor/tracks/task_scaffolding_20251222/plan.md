# Plan: Task Scaffolding Scripts

Implementation of CLI tools to generate boilerplate for services and commands.

## Phase 1: Foundation and Service Scaffolder
- [x] Task: Create `scripts/scaffold_utils.py` for shared logic (file writing, error handling).
- [x] Task: Implement `scripts/scaffold_service.py` with a basic template.
- [x] Task: Add standard `api_call` and `TypedDict` imports to the service template.
- [x] Task: Conductor - User Manual Verification 'Foundation and Service Scaffolder' (Protocol in workflow.md)

## Phase 2: CLI Scaffolder [checkpoint: fd2b137]
- [x] Task: Implement `scripts/scaffold_cli.py` with a Typer template. [693ab4b]
- [x] Task: Add standard CLI imports and basic command structure. [693ab4b]
- [x] Task: Implement the "Next Steps" reporting logic for both scripts. [693ab4b]
- [x] Task: Conductor - User Manual Verification 'CLI Scaffolder' (Protocol in workflow.md) [fd2b137]

## Phase 3: Integration and Refinement [checkpoint: aa6e26d]
- [x] Task: Add a "dry run" mode to scaffolding scripts (print to console instead of writing).
- [x] Task: Implement comprehensive error handling (e.g., invalid names, permission errors).
- [x] Task: Write unit tests in `tests/scripts/test_scaffolding.py`.
- [x] Task: Conductor - User Manual Verification 'Integration and Refinement' (Protocol in workflow.md) [aa6e26d]

## Phase 4: Verification [checkpoint: ac28d67]
- [x] Task: Use the new tool to scaffold a "Dummy" service and CLI command.
- [x] Task: Verify the generated code passes all lint/type checks.
- [x] Task: Conductor - User Manual Verification 'Verification' (Protocol in workflow.md) [ac28d67]
