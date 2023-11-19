import socket
import time
import logging

from .message_data_read_request import MessageDataReadRequest
from .message import Message

_LOGGER = logging.getLogger(__name__)


class Communication:
    @staticmethod
    def isOnline(ip: str, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            try:
                sock.connect((ip, port))
                return True
            except socket.error:
                return False

    @staticmethod
    def sendMessage(ip: str, port: int, message: Message) -> float:
        attempt = 1
        MAX_ATTEMPTS = 5
        while attempt <= MAX_ATTEMPTS:
            if attempt > 1:
                _LOGGER.debug(f"Attempt {attempt} of {MAX_ATTEMPTS}...")

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((ip, port))
                    _LOGGER.debug(f"Sending: {message.getRawDataBytes().decode('ascii')}")
                    sock.sendall(message.getRawDataBytes() + b"\n")
                    received = sock.recv(1024).decode("ascii").strip()
                    _LOGGER.debug(f"Received: {received}")
                    return received

            except socket.error as e:
                attempt += 1
                _LOGGER.debug(f"Socket error: {str(e)}")
                time.sleep(1)

        _LOGGER.error("Connection failed, no more attempts left")
        return None
