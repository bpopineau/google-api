from unittest.mock import MagicMock

import pytest

from mygooglib.workflows.search import global_search


def test_global_search_success():
    # Mock clients
    mock_clients = MagicMock()

    # Mock Drive
    mock_clients.drive.service = MagicMock()
    mock_clients.drive.service.files().list().execute.return_value = {
        "files": [
            {
                "id": "d1",
                "name": "File 1",
                "modifiedTime": "2023-01-01T00:00:00Z",
                "mimeType": "text/plain",
            }
        ]
    }
    # Direct call to list_files mock might be easier but let's assume we test the workflow interaction
    # Actually, global_search calls list_files which takes service object.

    from mygooglib.services import drive

    drive.list_files = MagicMock(
        return_value=[
            {
                "id": "d1",
                "name": "File 1",
                "modifiedTime": "2023-01-01T00:00:00Z",
                "mimeType": "text/plain",
            }
        ]
    )

    from mygooglib.services import gmail

    gmail.search_messages = MagicMock(
        return_value=[
            {
                "id": "g1",
                "subject": "Email 1",
                "snippet": "Hello world",
                "date": "Mon, 1 Jan 2023 00:00:00 +0000",
            }
        ]
    )

    results = global_search(mock_clients, "test", limit=5)

    assert len(results) == 2
    assert results[0]["type"] == "drive"
    assert results[0]["title"] == "File 1"
    assert results[1]["type"] == "gmail"
    assert results[1]["title"] == "Email 1"


def test_global_search_partial_failure():
    mock_clients = MagicMock()

    from mygooglib.services import drive

    drive.list_files = MagicMock(side_effect=Exception("Drive failure"))

    from mygooglib.services import gmail

    gmail.search_messages = MagicMock(
        return_value=[
            {
                "id": "g1",
                "subject": "Email 1",
                "snippet": "Hello world",
                "date": "Mon, 1 Jan 2023 00:00:00 +0000",
            }
        ]
    )

    results = global_search(mock_clients, "test", limit=5)

    assert len(results) == 1
    assert results[0]["type"] == "gmail"
