import pytest
from tests.factories.common import ColorFactory, DateFactory, SheetInfoFactory, MessageMetadataFactory
from tests.factories.drive import FileFactory
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
