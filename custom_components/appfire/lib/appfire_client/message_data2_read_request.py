from enum import IntEnum

from .message import Message

class MessageData2ReadRequest(Message):

    def __init__(self):
        super().__init__(Message.buildRawData("DAT", "R", ["2"]))
