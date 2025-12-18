---
description: Systematically refactor mygooglib code with safety checks
---

1. Verify Baseline
// turbo
   - `pytest`
   - `python scripts/smoke_test.py all`
   - **Constraint**: Do NOT proceed if tests or smoke tests fail.

2. Create Safety Checkpoint
   - `git add -A && git commit -m "checkpoint: before refactor"`

3. Scope and Plan
   - **Identify target**: Function/class/module in `mygooglib/`.
   - **Common refactor targets**:
     - `mygooglib/drive.py` — 19KB, largest module
     - `mygooglib/sheets.py` — 22KB, complex A1 logic
     - `mygooglib/gmail.py` — 15KB, MIME handling
   - **Code smells to look for**:
     - Duplicated patterns across services
     - Long methods (extract to `mygooglib/utils/`)
     - Magic strings/numbers (extract to constants)
   - **Breaking changes**: If modifying public API (functions in `__all__`), add deprecation warning.

4. Execute Refactor
   - **Incremental**: Change one method/class at a time.
   - **Test frequently**: Run `pytest` after each logical chunk.

5. Verify Changes
// turbo
   - `ruff format . && ruff check . --fix`
   - `pytest`
   - `python scripts/smoke_test.py all`
   - **Logic**: Refactoring shouldn't change behavior.

6. Update Documentation
   - If signature changed, update `docs/guides/usage.md`.
   - If internal architecture changed, update `docs/reference/design_principles.md`.
   - Run `/write_docstrings` if docstrings need updating.

7. Cleanup
   - Remove unused imports (`ruff check . --select F401`).
   - Delete temporary scaffolding.
