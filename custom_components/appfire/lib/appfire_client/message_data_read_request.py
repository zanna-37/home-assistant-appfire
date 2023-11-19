from enum import IntEnum

from .message import Message

class MessageDataReadRequest(Message):

    def __init__(self):
        super().__init__(Message.buildRawData("DAT", "R", ["0"]))
