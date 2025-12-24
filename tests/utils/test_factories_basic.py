import pytest
from tests.factories.common import ColorFactory, DateFactory, SheetInfoFactory, MessageMetadataFactory

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
