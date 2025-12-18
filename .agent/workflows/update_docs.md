---
description: Meticulously update mygooglib documentation to ensure accuracy
---

1. Audit Recent Code Changes
   - `git log -p -10 --oneline mygooglib/`
   - **Look for**: New methods, changed signatures, removed functions.

2. Verify API Reference Matches Code
   - **Check docstrings render correctly**:
     - `python -m pydoc mygooglib.drive`
     - `python -m pydoc mygooglib.sheets`
     - `python -m pydoc mygooglib.gmail`
     - `python -m pydoc mygooglib.calendar`
     - `python -m pydoc mygooglib.tasks`
     - `python -m pydoc mygooglib.docs`
   - **Update**: `docs/reference/design_principles.md` if architecture changed.

3. Update Guides
   - **File**: `docs/guides/usage.md`
     - Verify all code examples still work.
     - Add examples for new methods.
   - **File**: `docs/guides/configuration.md`
     - Verify OAuth scopes are accurate.
     - Check environment variable names.

4. Verify Examples Run
// turbo
   - `python examples/drive_list_files.py`
   - `python examples/sheets_read_by_title.py`
   - `python examples/gmail_send_email.py` (careful: sends real email!)
   - **Fix or update**: Any broken examples.

5. Maintain Consistency
   - **README.md**: Does Quick Start still work?
   - **AUTOMATION_GOALS.md**: Is Must/Nice/Later accurate?
   - **CHANGELOG.md**: Is latest version documented?
   - `docs/development/roadmap.md`: Update progress checkboxes.

6. Check CLI Documentation
   - `mygoog --help` — verify top-level help is clear.
   - `mygoog drive --help`, `mygoog sheets --help`, etc.
   - Update docs if CLI interface changed.

7. Final Review
   - Read `README.md` as a new user.
   - **Question**: "Can someone use mygooglib from just the README?"
