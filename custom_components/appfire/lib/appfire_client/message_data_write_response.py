from enum import IntEnum

from .message import Message


class MessageDataWriteResponse(Message):
    def __init__(self, rawData):
        super().__init__(rawData)

    def isWriteSuccessful(self) -> bool:
        payload = self.getPayload()
        if payload is None:
            return False
        elif len(payload) == 0:
            return False
        else:
            return payload[0] == "OK"
