import logging

from .communication import Communication
from .message import ChecksumError
from .message_data_read_request import MessageDataReadRequest
from .message_data_read_response import MessageDataReadResponse
from .message_data_write_request import MessageDataWriteRequest
from .message_data_write_response import MessageDataWriteResponse
from .message_data2_read_request import MessageData2ReadRequest
from .message_data2_read_response import MessageData2ReadResponse

_LOGGER = logging.getLogger(__name__)


# a class that takes ip and port as constructor arguments
class AppFire:
    """AppFire integration."""

    def __init__(self, ip, port):
        """Initialize AppFire."""
        self.ip = ip
        self.port = port

    def getMessageInfo(self) -> MessageDataReadResponse:
        message = MessageDataReadRequest()
        response = Communication.sendMessage(self.ip, self.port, message)

        try:
            info = MessageDataReadResponse(response)
        except ChecksumError as e:
            _LOGGER.error(f"Message error: {str(e)}")
            return None
        else:
            return info

    def getMessage2Info(self) -> MessageData2ReadResponse:
        message = MessageData2ReadRequest()
        response = Communication.sendMessage(self.ip, self.port, message)

        try:
            info = MessageData2ReadResponse(response)
        except ChecksumError as e:
            _LOGGER.error(f"Message error: {str(e)}")
            return None
        else:
            return info

    def isOnline(self) -> bool:
        return Communication.isOnline(self.ip, self.port)

    def turnOn(self):
        messageTurnOn = MessageDataWriteRequest(
            MessageDataWriteRequest.buildRawDataSetPowerStatus(True)
        )
        response = Communication.sendMessage(self.ip, self.port, messageTurnOn)

        try:
            writeResponse = MessageDataWriteResponse(response)
        except ChecksumError as e:
            _LOGGER.error(f"Message error: {str(e)}")
            return None
        else:
            if not writeResponse.isWriteSuccessful():
                raise Exception("Failed to turn on")  # TODO add retry

    def turnOff(self):
        messageTurnOff = MessageDataWriteRequest(
            MessageDataWriteRequest.buildRawDataSetPowerStatus(False)
        )
        response = Communication.sendMessage(self.ip, self.port, messageTurnOff)

        try:
            writeResponse = MessageDataWriteResponse(response)
        except ChecksumError as e:
            _LOGGER.error(f"Message error: {str(e)}")
            return None
        else:
            if not writeResponse.isWriteSuccessful():
                raise Exception("Failed to turn off")  # TODO add retry

    def setDesiredAmbientTemperature(self, temperature: float):
        messageSetDesiredAmbientTemperature = MessageDataWriteRequest(
            MessageDataWriteRequest.buildRawDataSetDesiredAmbientTemperature(
                temperature
            )
        )
        response = Communication.sendMessage(
            self.ip, self.port, messageSetDesiredAmbientTemperature
        )

        try:
            writeResponse = MessageDataWriteResponse(response)
        except ChecksumError as e:
            _LOGGER.error(f"Message error: {str(e)}")
            return None
        else:
            if not writeResponse.isWriteSuccessful():
                raise Exception("Failed to set desired ambient temperature")
