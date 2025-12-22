from __future__ import annotations

from mygooglib import get_clients
from mygooglib.services.sheets import get_range

# Replace with your spreadsheet title, ID, or full URL.
SPREADSHEET = "Your Sheet Title"
RANGE = "Sheet1!A1:C10"


def main() -> int:
    clients = get_clients()

    values = get_range(
        clients.sheets,
        SPREADSHEET,
        RANGE,
        drive=clients.drive,  # required if SPREADSHEET is a title
    )

    print(values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


