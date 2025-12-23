# Audit Report: scripts/scaffold_utils.py

## Purpose
- Shared utility functions for project-wide scaffolding tools.

## Findings
- **Robust Path Resolution:** Correctly identifies the project root by searching for `pyproject.toml`.
- **Safety:** Implements mandatory name validation (snake_case) and a versatile `write_file` worker with overwrite protection and dry-run support.

## Quality Checklist
- [x] Functional project root discovery
- [x] Robust file writer with dry-run support
