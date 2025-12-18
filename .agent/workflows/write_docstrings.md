---
description: Write and enforce Google-style docstrings
---

1. Select Target
   - **Action**: Identify the function, class, or module needing documentation.

2. Write Docstring (Google Style)
   - **Format**:
     ```python
     """Short summary.

     Longer explanation if needed.

     Args:
         arg_name (type): Description.

     Returns:
         type: Description.

     Raises:
         ErrorType: Description.
     """
     ```
   - **Tip**: Be concise. Describe *what* and *why*, not *how*.

3. Verify Format
   - **Action**: Run ruff with pydocstyle rules enabled for this file.
   - `ruff check path/to/file.py --select D --ignore D100,D104` (Adjust ignores as needed)
   - **Goal**: Ensure no linting errors regarding formatting (e.g., missing period, blank lines).

4. Verify Clarity (Human Review)
   - **Question**: "Does this explain how to use the function without reading the code?"
