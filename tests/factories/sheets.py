from polyfactory.factories.typed_dict_factory import TypedDictFactory
from mygooglib.core.types import SpreadsheetDict, SheetDict, ValueRangeDict, SpreadsheetPropertiesDict, SheetPropertiesDict

class SpreadsheetPropertiesFactory(TypedDictFactory[SpreadsheetPropertiesDict]):
    __model__ = SpreadsheetPropertiesDict
    title = "Test Spreadsheet"
    locale = "en_US"
    timeZone = "UTC"

class SheetPropertiesFactory(TypedDictFactory[SheetPropertiesDict]):
    __model__ = SheetPropertiesDict
    sheetId = 0
    title = "Sheet1"
    index = 0
    sheetType = "GRID"

class SheetFactory(TypedDictFactory[SheetDict]):
    __model__ = SheetDict
    properties = SheetPropertiesFactory.build()

class SpreadsheetFactory(TypedDictFactory[SpreadsheetDict]):
    __model__ = SpreadsheetDict
    spreadsheetId = "sheet123"
    properties = SpreadsheetPropertiesFactory.build()
    sheets = [SheetFactory.build()]
    spreadsheetUrl = "https://docs.google.com/spreadsheets/d/sheet123/edit"

class ValueRangeFactory(TypedDictFactory[ValueRangeDict]):
    __model__ = ValueRangeDict
    range = "Sheet1!A1:B2"
    majorDimension = "ROWS"
    values = [["A1", "B1"], ["A2", "B2"]]
