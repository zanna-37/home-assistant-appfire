import random

from .crc.crc16_ccitt_false import Crc16_ccitt_false


class Message:
    def __init__(self, rawData):
        self.rawData = rawData
        if not self.isCrcValid():
            raise ChecksumError("Checksum is not valid")

    @staticmethod
    def buildRawData(payloadType, operationType, payloadList):
        payload = ";".join(payloadList) + ";"

        rawData = Message._generateRandomMessageId()
        rawData += "---"
        rawData += str(format(len(payload), "04x"))
        rawData += payloadType
        rawData += operationType
        rawData += payload

        checksum = format(
            Crc16_ccitt_false.crc_from(bytes(rawData, "ascii")), "04x"
        ).upper()

        # Prepend the '#' character
        rawData = "#" + rawData + checksum

        return rawData

    def getMessageId(self):
        if self.rawData is None:
            return None
        else:
            return self.rawData[1:7]

    def getPayloadLength(self) -> int:
        if self.rawData is None:
            return None
        else:
            return int(self.rawData[10:14], 16)

    def getPayloadType(self):
        if self.rawData is None:
            return None
        else:
            return self.rawData[14:17]

    def getOperationType(self):
        if self.rawData is None:
            return None
        else:
            return self.rawData[17:18]

    def getPayload(self):
        if self.rawData is None:
            return None
        else:
            return self._getRawPayload().split(";")

    def getCrc(self):
        if self.rawData is None:
            return None
        else:
            return int(self.rawData[18 + self.getPayloadLength() :], 16)

    def isCrcValid(self):
        if self.rawData is None:
            return false
        else:
            return self._calculateCrc() == self.getCrc()

    def getRawDataBytes(self):
        if self.rawData is None:
            return None
        else:
            return bytes(self.rawData, "ascii")

    # private methods

    def _getRawPayload(self):
        if self.rawData is None:
            return None
        else:
            return self.rawData[18 : 18 + self.getPayloadLength()]

    def _calculateCrc(self):
        if self.rawData is None:
            return None
        else:
            data = self.rawData[1 : 18 + self.getPayloadLength()]
            return Crc16_ccitt_false.crc_from(bytes(data, "ascii"))

    @staticmethod
    def _generateRandomMessageId():
        return str(random.randint(0, 999999)).zfill(6)


class ChecksumError(Exception):
    pass
