from enum import IntEnum

from .message import Message


class Index(IntEnum):
    FAN1_PERCENTAGE_INDEX = 3


class MessageData2ReadResponse(Message):
    def __init__(self, rawData):
        super().__init__(rawData)

    def getFan1Percentage(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.FAN1_PERCENTAGE_INDEX])
