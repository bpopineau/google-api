from __future__ import annotations

from mygooglib import get_clients
from mygooglib.services.drive import list_files

# Optional query examples:
# - "name contains 'report'"
# - "mimeType = 'application/pdf'"
QUERY: str | None = "name contains 'report'"

# Optional: only list files under a folder.
PARENT_ID: str | None = None


def main() -> int:
    clients = get_clients()

    files = list_files(
        clients.drive,
        query=QUERY,
        parent_id=PARENT_ID,
    )

    for f in files:
        print(f.get("id"), f.get("name"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


