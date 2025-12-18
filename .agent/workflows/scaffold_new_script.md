---
description: Create a new mygooglib automation script with boilerplate
---

1. Choose Location and Name
   - **Scripts**: `scripts/` — for internal tools and maintenance.
   - **Examples**: `examples/` — for user-facing demos.
   - **Naming**: Use `snake_case.py` (e.g., `drive_backup_photos.py`).

2. Create File with mygooglib Boilerplate
   - **Template**:
     ```python
     """[Short description of what this script does].

     Usage:
         python scripts/your_script.py
     """
     from __future__ import annotations

     from mygooglib import get_clients


     def main() -> int:
         clients = get_clients()

         # Available clients:
         # - clients.drive   (list_files, upload_file, download_file, sync_folder, find_by_name)
         # - clients.sheets  (get_range, update_range, append_row, open_by_title)
         # - clients.gmail   (send_email, search_messages, mark_read)
         # - clients.calendar (add_event, list_events, update_event, delete_event)
         # - clients.tasks   (list_tasklists, list_tasks, add_task, complete_task)
         # - clients.docs    (create, get_text, append_text, render_template)

         # Your logic here
         # ...

         return 0


     if __name__ == "__main__":
         raise SystemExit(main())
     ```

3. Run Initial Test
   - `python scripts/your_script.py`
   - **Goal**: Verify it imports and authenticates without error.

4. Add to Smoke Test (optional)
   - If this script is a new command, consider adding it to `scripts/smoke_test.py`.
   - Follow the existing `argparse` subparser pattern.

5. Document
   - Add entry to `docs/guides/usage.md` if user-facing.
   - Add to `examples/` README if it's a demo script.
