from polyfactory.factories.typed_dict_factory import TypedDictFactory
from mygooglib.core.types import (
    LabelDict,
    MessageDict,
    ThreadDict,
    MessagePartDict,
    MessagePartBodyDict,
    HeaderDict,
)

class LabelFactory(TypedDictFactory[LabelDict]):
    __model__ = LabelDict
    id = "INBOX"
    name = "INBOX"
    type = "system"

class HeaderFactory(TypedDictFactory[HeaderDict]):
    __model__ = HeaderDict
    name = "Subject"
    value = "Test Subject"

class MessagePartBodyFactory(TypedDictFactory[MessagePartBodyDict]):
    __model__ = MessagePartBodyDict
    size = 100
    data = "SGVsbG8gV29ybGQ="  # "Hello World" in base64

class MessagePartFactory(TypedDictFactory[MessagePartDict]):
    __model__ = MessagePartDict
    partId = "0"
    mimeType = "text/plain"
    filename = ""
    headers = [HeaderFactory.build()]
    body = MessagePartBodyFactory.build()
    parts = []

class MessageFactory(TypedDictFactory[MessageDict]):
    __model__ = MessageDict
    id = "msg123"
    threadId = "thread123"
    labelIds = ["INBOX"]
    snippet = "Hello World"
    payload = MessagePartFactory.build()

class ThreadFactory(TypedDictFactory[ThreadDict]):
    __model__ = ThreadDict
    id = "thread123"
    snippet = "Hello World"
    messages = [MessageFactory.build()]
