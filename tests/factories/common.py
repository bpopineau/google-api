from polyfactory.factories.typed_dict_factory import TypedDictFactory

from mygooglib.core.types import (
    AttachmentMetadataDict,
    ColorDict,
    DateDict,
    MessageFullDict,
    MessageMetadataDict,
    SheetInfoDict,
)


class ColorFactory(TypedDictFactory[ColorDict]):
    __model__ = ColorDict
    red = 0.0
    green = 0.0
    blue = 0.0
    alpha = 1.0


class DateFactory(TypedDictFactory[DateDict]):
    __model__ = DateDict
    year = 2025
    month = 12
    day = 23


class SheetInfoFactory(TypedDictFactory[SheetInfoDict]):
    __model__ = SheetInfoDict
    title = "Sheet1"
    id = 0
    index = 0
    type = "GRID"


class MessageMetadataFactory(TypedDictFactory[MessageMetadataDict]):
    __model__ = MessageMetadataDict
    id = "msg123"
    threadId = "thread123"
    subject = "Test Subject"
    from_ = "sender@example.com"
    to = "recipient@example.com"
    date = "2025-12-23T10:00:00Z"
    snippet = "This is a snippet"
    labelIds = ["INBOX"]
    hasAttachment = False
    isUnread = True
    title = "Test Subject"


class AttachmentMetadataFactory(TypedDictFactory[AttachmentMetadataDict]):
    __model__ = AttachmentMetadataDict
    filename = "attachment.txt"
    attachment_id = "attach123"
    mime_type = "text/plain"
    size = 1024


class MessageFullFactory(TypedDictFactory[MessageFullDict]):
    __model__ = MessageFullDict
    id = "msg123"
    threadId = "thread123"
    subject = "Test Subject"
    from_ = "sender@example.com"
    to = "recipient@example.com"
    date = "2025-12-23T10:00:00Z"
    snippet = "This is a snippet"
    body = "This is the message body"
    labelIds = ["INBOX"]
    attachments: list[AttachmentMetadataDict] = []
