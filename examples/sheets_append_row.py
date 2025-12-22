from __future__ import annotations

from mygooglib import get_clients
from mygooglib.services.sheets import append_row

# Replace with your spreadsheet title, ID, or full URL.
SPREADSHEET = "Your Sheet Title"
TAB = "Sheet1"


def main() -> int:
    clients = get_clients()

    result = append_row(
        clients.sheets,
        SPREADSHEET,
        TAB,
        ["a", "b", "c"],
        drive=clients.drive,  # required if SPREADSHEET is a title
    )

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
