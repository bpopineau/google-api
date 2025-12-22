"""Test Global Search logic."""

from unittest.mock import MagicMock, patch

import pytest

from mygoog_gui.pages.home import HomePage


@pytest.fixture
def mock_clients():
    clients = MagicMock()
    clients.drive.list_files.return_value = [
        {
            "id": "1",
            "name": "Test Doc",
            "mimeType": "application/vnd.google-apps.document",
        }
    ]
    clients.gmail.search_messages.return_value = [
        {
            "id": "100",
            "subject": "Test Email",
            "snippet": "Hello",
            "from": "test@example.com",
        }
    ]
    return clients


def test_on_search_calls_apis(qapp, mock_clients):
    """Verify that searching triggers both Drive and Gmail APIs.

    The qapp fixture ensures QApplication exists (required for QWidgets).
    """
    # We mock ApiWorker to run synchronously for testing
    with patch("mygoog_gui.pages.home.ApiWorker") as MockWorker:
        # A cleaner way: Mock the worker instance returned by the class
        mock_worker_instance = MockWorker.return_value

        def run_worker_logic():
            # The 'func' passed to ApiWorker constructor
            worker_func = MockWorker.call_args[0][0]
            # Execute logic
            result = worker_func()
            return result

        mock_worker_instance.start.side_effect = run_worker_logic

        # Mock UI setup to avoid slow Qt widget creation
        with (
            patch.object(HomePage, "_setup_ui"),
            patch.object(HomePage, "_load_dashboard_data"),
        ):
            page = HomePage(mock_clients)

            # Setup inputs manually since _setup_ui is mocked
            page.search_input = MagicMock()
            page.search_input.text.return_value = "test"
            page.stack = MagicMock()
            page.results_header = MagicMock()
            page.search_drive_list = MagicMock()
            page.search_gmail_list = MagicMock()
            page._clear_layout = MagicMock()
            page._workers = []

            # Trigger search
            page._on_search()

            # Verify API calls were made by the worker logic
            mock_clients.drive.list_files.assert_called_with(
                query="name contains 'test'", page_size=10
            )
            mock_clients.gmail.search_messages.assert_called_with(
                query="test", max_results=10
            )


