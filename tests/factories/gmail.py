from polyfactory import Use
from polyfactory.decorators import post_generated
from polyfactory.factories.typed_dict_factory import TypedDictFactory

from mygooglib.core.types import (
    HeaderDict,
    LabelDict,
    MessageDict,
    MessagePartBodyDict,
    MessagePartDict,
    ThreadDict,
)


class LabelFactory(TypedDictFactory[LabelDict]):
    __model__ = LabelDict


class HeaderFactory(TypedDictFactory[HeaderDict]):
    __model__ = HeaderDict
    name = "Subject"
    value = "Test"


class MessagePartBodyFactory(TypedDictFactory[MessagePartBodyDict]):
    __model__ = MessagePartBodyDict
    size = 0


class MessagePartFactory(TypedDictFactory[MessagePartDict]):
    __model__ = MessagePartDict
    partId = "0"
    mimeType = "text/plain"
    filename = ""
    body = Use(MessagePartBodyFactory.build)
    parts = Use(list)  # type: ignore[var-annotated]


class MessageFactory(TypedDictFactory[MessageDict]):
    __model__ = MessageDict
    id = "msg123"
    threadId = "thread123"
    snippet = ""

    @post_generated
    @classmethod
    def payload(cls, payload: MessagePartDict | None = None) -> MessagePartDict:
        return payload or MessagePartFactory.build()

    # Ensure payload can be overridden


class ThreadFactory(TypedDictFactory[ThreadDict]):
    __model__ = ThreadDict
    id = "thread123"
    snippet = ""

    @post_generated
    @classmethod
    def messages(cls, messages: list[MessageDict] | None = None) -> list[MessageDict]:
        return messages or MessageFactory.batch(size=1)
