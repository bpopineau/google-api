"""Test Global Search logic."""

from unittest.mock import MagicMock, patch

import pytest

from mygoog_gui.pages.home import HomePage
from tests.factories.drive import FileFactory
from tests.factories.common import MessageMetadataFactory


@pytest.fixture
def mock_clients():
    clients = MagicMock()
    clients.drive.list_files.return_value = [
        FileFactory.build(
            id="1",
            name="Test Doc",
            mimeType="application/vnd.google-apps.document",
        )
    ]
    clients.gmail.search_messages.return_value = [
        MessageMetadataFactory.build(
            id="100",
            subject="Test Email",
            snippet="Hello",
            from_="test@example.com",
        )
    ]
    return clients


def test_on_search_calls_apis(qapp, mock_clients):
    """Verify that searching triggers global_search workflow."""
    # Patch the global_search function used in the home page
    with patch("mygoog_gui.pages.home.global_search") as mock_search:
        mock_search.return_value = [
            {"type": "drive", "id": "1", "title": "Test Doc"},
            {"type": "gmail", "id": "100", "title": "Test Email"},
        ]

        # Mock ApiWorker to run synchronously
        with patch("mygoog_gui.pages.home.ApiWorker") as MockWorker:
            mock_worker_instance = MockWorker.return_value

            def run_worker_logic():
                worker_func = MockWorker.call_args[0][0]
                result = worker_func()
                # Manually emit finished signal since we are mocking the worker
                # In real app, the thread emits this.
                # But here we are just testing that logic runs.
                # Actually, the test just checked api calls before.
                # Now we check global_search call.
                return result

            mock_worker_instance.start.side_effect = run_worker_logic

            # Mock UI setup
            with (
                patch.object(HomePage, "_setup_ui"),
                patch.object(HomePage, "_load_dashboard_data"),
            ):
                page = HomePage(mock_clients)

                # Setup manual UI elements
                page.search_input = MagicMock()
                page.search_input.text.return_value = "test"
                page.stack = MagicMock()
                page.results_header = MagicMock()
                page.search_drive_list = MagicMock()
                page.search_gmail_list = MagicMock()
                page._clear_layout = MagicMock()  # type: ignore[method-assign]
                page._workers = []

                # Trigger search
                page._on_search()

                # Verify global_search was called
                mock_search.assert_called_once()
                args, kwargs = mock_search.call_args
                # args[0] is clients, args[1] is query
                assert args[0] == mock_clients
                assert args[1] == "test"
