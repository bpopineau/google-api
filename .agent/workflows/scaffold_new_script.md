---
description: Create a new automation script with boilerplate
---

1. Choose a Name
   - **Constraint**: Use snake_case.
   - **Location**: `scripts/` (or `examples/` if it's a demo).

2. Create File
   - **Template**:
     ```python
     from __future__ import annotations
     from mygooglib import get_clients

     def main() -> int:
         clients = get_clients()
         # Your logic here
         # ...
         return 0

     if __name__ == "__main__":
         raise SystemExit(main())
     ```

3. Make Executable (optional)
   - If on Linux/Mac, `chmod +x scripts/your_script.py`.

4. Run Initial Test
   - `python scripts/your_script.py`
   - **Goal**: Ensure it imports and connects without error.
