from __future__ import annotations

from mygooglib import get_clients
from mygooglib.drive import sync_folder

# Replace with a real local folder path on your machine.
LOCAL_PATH = r"C:\path\to\folder"

# Replace with a real Drive folder id.
DRIVE_FOLDER_ID = "<FOLDER_ID>"


def main() -> int:
    clients = get_clients()

    summary = sync_folder(
        clients.drive,
        LOCAL_PATH,
        DRIVE_FOLDER_ID,
    )

    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
