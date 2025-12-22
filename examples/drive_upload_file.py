from __future__ import annotations

from mygooglib import get_clients
from mygooglib.services.drive import upload_file

# Replace with a real file path on your machine.
LOCAL_PATH = r"C:\path\to\file.pdf"

# Optional: Drive folder id to upload into (None = My Drive root)
PARENT_ID: str | None = None


def main() -> int:
    clients = get_clients()

    file_id = upload_file(
        clients.drive,
        LOCAL_PATH,
        parent_id=PARENT_ID,
    )

    print(file_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
