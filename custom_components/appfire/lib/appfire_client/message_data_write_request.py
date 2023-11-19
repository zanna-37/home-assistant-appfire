from enum import IntEnum

from .message import Message


class Index(IntEnum):
    POWER_STATUS_INDEX = 0
    TEMPERATURE_INDEX = 3

class MessageDataWriteRequest(Message):
    def __init__(self, rawData):
        super().__init__(rawData)

    @staticmethod
    def buildRawDataSetPowerStatus(statusOn: bool):
        return Message.buildRawData("DAT", "W", [str(Index.POWER_STATUS_INDEX), "1" if statusOn else "0"])

    @staticmethod
    def buildRawDataSetDesiredAmbientTemperature(temperature: float):
        return Message.buildRawData("DAT", "W", [str(Index.TEMPERATURE_INDEX), str(int(temperature * 10))])
