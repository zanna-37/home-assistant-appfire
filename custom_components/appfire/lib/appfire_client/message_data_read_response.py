from enum import IntEnum

from .message import Message


class Index(IntEnum):
    STATUS_INDEX = 5
    POWER_INDEX = 6
    ECO_MODE_INDEX = 7
    CRONO_MODE_INDEX = 8
    AMBIENT_TEMPERATURE_INDEX = 9
    DESIRED_AMBIENT_TEMPERATURE_INDEX = 10
    DESIRED_AMBIENT_TEMPERATURE_MIN_INDEX = 11
    DESIRED_AMBIENT_TEMPERATURE_MAX_INDEX = 12
    SMOKE_TEMPERATURE_INDEX = 21
    POWER_PERCENTAGE_INDEX = 22
    DESIRED_MAX_POWER_PERCENTAGE_INDEX = 23
    DESIRED_MAX_POWER_LEVEL_MIN_INDEX = 24
    DESIRED_MAX_POWER_LEVEL_MAX_INDEX = 25
    SMOKE_FAN_RPM_INDEX = 26


class MessageDataReadResponse(Message):
    def __init__(self, rawData):
        super().__init__(rawData)

    def getStatus(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.STATUS_INDEX])

    def isOn(self) -> bool:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.POWER_INDEX]) == 1

    def isEcoMode(self) -> bool:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.ECO_MODE_INDEX]) == 1

    def getCronoMode(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.CRONO_MODE_INDEX])

    def getAmbientTemperature(self) -> float:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.AMBIENT_TEMPERATURE_INDEX]) / 10

    def getDesiredAmbientTemperature(self) -> float:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.DESIRED_AMBIENT_TEMPERATURE_INDEX]) / 10

    def getDesiredAmbientTemperatureMin(self) -> float:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return (
                int(self.getPayload()[Index.DESIRED_AMBIENT_TEMPERATURE_MIN_INDEX]) / 10
            )

    def getDesiredAmbientTemperatureMax(self) -> float:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return (
                int(self.getPayload()[Index.DESIRED_AMBIENT_TEMPERATURE_MAX_INDEX]) / 10
            )

    def getSmokeTemperature(self) -> float:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.SMOKE_TEMPERATURE_INDEX]) / 10

    def getPowerPercentage(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.POWER_PERCENTAGE_INDEX])

    def getDesiredMaxPowerPercentage(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.DESIRED_MAX_POWER_PERCENTAGE_INDEX])

    def getDesiredMaxPowerPercentageMin(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.DESIRED_MAX_POWER_LEVEL_MIN_INDEX])

    def getDesiredMaxPowerPercentageMax(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.DESIRED_MAX_POWER_LEVEL_MAX_INDEX])

    def getSmokeFanRpm(self) -> int:
        payload = self.getPayload()
        if payload is None:
            return None
        else:
            return int(self.getPayload()[Index.SMOKE_FAN_RPM_INDEX])
