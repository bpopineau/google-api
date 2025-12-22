from unittest.mock import MagicMock, patch


from mygooglib.workflows.search import global_search


def test_global_search_success():
    # Mock clients
    mock_clients = MagicMock()
    # Ensure service mocks are cleaner (though patched functions won't use them if we patch well)
    mock_clients.drive.service = MagicMock()

    # Data to return
    drive_files = [
        {
            "id": "d1",
            "name": "File 1",
            "modifiedTime": "2023-01-01T00:00:00Z",
            "mimeType": "text/plain",
        }
    ]
    gmail_msgs = [
        {
            "id": "g1",
            "subject": "Email 1",
            "snippet": "Hello world",
            "date": "Mon, 1 Jan 2023 00:00:00 +0000",
        }
    ]

    with patch(
        "mygooglib.workflows.search.list_files", return_value=drive_files
    ) as mock_list:
        with patch(
            "mygooglib.workflows.search.search_messages", return_value=gmail_msgs
        ) as mock_search:
            results = global_search(mock_clients, "test", limit=5)

            assert len(results) == 2
            assert results[0]["type"] == "drive"
            assert results[0]["title"] == "File 1"
            assert results[1]["type"] == "gmail"
            assert results[1]["title"] == "Email 1"

            mock_list.assert_called_once()
            mock_search.assert_called_once()


def test_global_search_partial_failure():
    mock_clients = MagicMock()

    with patch(
        "mygooglib.workflows.search.list_files", side_effect=Exception("Drive failure")
    ):
        with patch(
            "mygooglib.workflows.search.search_messages",
            return_value=[
                {
                    "id": "g1",
                    "subject": "Email 1",
                    "snippet": "Hello world",
                    "date": "Mon, 1 Jan 2023 00:00:00 +0000",
                }
            ],
        ):
            results = global_search(mock_clients, "test", limit=5)

            assert len(results) == 1
            assert results[0]["type"] == "gmail"
