from polyfactory.factories.typed_dict_factory import TypedDictFactory
from mygooglib.core.types import FileDict

class FileFactory(TypedDictFactory[FileDict]):
    __model__ = FileDict

    id = "file123"
    name = "test_file.txt"
    mimeType = "text/plain"
    modifiedTime = "2025-12-23T10:00:00.000Z"
    size = "1024"
    parents = ["root"]
    trashed = False
    kind = "drive#file"
