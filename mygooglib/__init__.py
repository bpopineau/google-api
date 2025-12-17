"""Personal Google APIs wrapper library.

Quick start:
    from mygooglib import get_clients
    clients = get_clients()
    clients.drive.upload_file(...)
"""

from mygooglib.auth import get_creds
from mygooglib.client import get_clients

__all__ = ["get_creds", "get_clients"]
