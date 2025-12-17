"""Personal Google APIs wrapper library.

Quick start:
    from mygooglib import get_clients
    clients = get_clients()
    # Drive helpers are free functions that take the raw service Resource:
    from mygooglib.drive import upload_file
    file_id = upload_file(clients.drive, "./report.pdf")
"""

from mygooglib.auth import get_creds
from mygooglib.client import get_clients

__all__ = ["get_creds", "get_clients"]
