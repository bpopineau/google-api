
from tests.factories.common import (
    ColorFactory,
    DateFactory,
    MessageMetadataFactory,
    SheetInfoFactory,
)
from tests.factories.drive import FileFactory
from tests.factories.gmail import MessageFactory, ThreadFactory
from tests.factories.sheets import SpreadsheetFactory, ValueRangeFactory


def test_color_factory():
    color = ColorFactory.build()
    assert "red" in color
    assert isinstance(color["red"], float)


def test_date_factory():
    date = DateFactory.build()
    assert "year" in date
    assert isinstance(date["year"], int)


def test_sheet_info_factory():
    info = SheetInfoFactory.build()
    assert "title" in info
    assert "id" in info


def test_message_metadata_factory():
    meta = MessageMetadataFactory.build()
    assert "id" in meta
    assert "subject" in meta
    assert "from_" in meta


def test_factory_overrides():
    color = ColorFactory.build(red=1.0, blue=0.5)
    assert color["red"] == 1.0
    assert color["blue"] == 0.5
    assert color["green"] == 0.0  # Default remains


def test_file_factory():
    file_meta = FileFactory.build()
    assert "id" in file_meta
    assert "name" in file_meta
    assert file_meta["mimeType"] == "text/plain"


def test_sheets_factories():
    ss = SpreadsheetFactory.build()
    assert ss["spreadsheetId"] == "sheet123"
    assert ss["properties"]["title"] == "Test Spreadsheet"

    vr = ValueRangeFactory.build()
    assert "values" in vr
    assert len(vr["values"]) == 2


def test_gmail_factories():
    msg = MessageFactory.build()
    assert msg["id"] == "msg123"
    assert "payload" in msg
    assert msg["payload"]["mimeType"] == "text/plain"

    thread = ThreadFactory.build()
    assert thread["id"] == "thread123"
    assert len(thread["messages"]) == 1
    assert thread["messages"][0]["id"] == "msg123"


def test_types_validation():
    # Verify that types are correct
    color = ColorFactory.build()
    assert isinstance(color["red"], (float, int))

    date = DateFactory.build()
    assert isinstance(date["year"], int)

    file_meta = FileFactory.build()
    assert isinstance(file_meta["id"], str)
    assert isinstance(file_meta["parents"], list)


def test_message_factory_nested_override():
    """Verify that nested overrides (payload) are respected."""
    custom_payload = {
        "mimeType": "application/json",
        "partId": "99",
        "filename": "test.json",
        "body": {"size": 10},
        "parts": [],
    }
    # ignore: type error because TypedDict factory build args are kwargs
    msg_replaced = MessageFactory.build(payload=custom_payload)  # type: ignore

    assert msg_replaced["payload"]["mimeType"] == "application/json"
    assert msg_replaced["payload"]["filename"] == "test.json"


def test_thread_factory_list_generation():
    """Verify ThreadFactory generates a list of messages."""
    thread = ThreadFactory.build()
    assert isinstance(thread["messages"], list)
    assert len(thread["messages"]) > 0
    assert "id" in thread["messages"][0]
