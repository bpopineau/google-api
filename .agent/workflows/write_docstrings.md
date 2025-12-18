---
description: Write and enforce Google-style docstrings for mygooglib
---

1. Select Target
   - **Priority order for mygooglib**:
     1. Public API in `mygooglib/__init__.py` (`get_clients`, `get_creds`)
     2. Client methods in `mygooglib/[service].py`
     3. CLI commands in `mygooglib/cli/[service].py`
     4. Utilities in `mygooglib/utils/`

2. Write Docstring (Google Style)
   - **Format**:
     ```python
     def upload_file(
         self,
         local_path: str | Path,
         parent_id: str | None = None,
         name: str | None = None,
     ) -> str:
         """Upload a local file to Google Drive.

         Args:
             local_path: Path to the local file to upload.
             parent_id: Optional Drive folder ID to upload into.
                 Defaults to root if not specified.
             name: Optional name for the file in Drive.
                 Defaults to the local filename.

         Returns:
             The Drive file ID of the uploaded file.

         Raises:
             FileNotFoundError: If local_path does not exist.
             DriveError: If the upload fails.
         """
     ```
   - **Tip**: Describe *what* and *why*, not implementation details.

3. Common mygooglib Patterns
   - **Identifier resolution**: Many methods accept ID, title, or URL.
     ```python
     """
     Args:
         identifier: Spreadsheet ID, title, or full URL.
             Titles are resolved via Drive API lookup.
     """
     ```
   - **Client references**: Note which underlying Google API is used.

4. Verify Format
// turbo
   - `ruff check mygooglib/ --select D --ignore D100,D104`
   - **D100**: Missing module docstring (ignore for `__init__.py`)
   - **D104**: Missing package docstring (ignore)

5. Verify Clarity
   - **Question**: "Does this explain how to use the method without reading the code?"
   - **Test**: `python -m pydoc mygooglib.[module].[function]`
