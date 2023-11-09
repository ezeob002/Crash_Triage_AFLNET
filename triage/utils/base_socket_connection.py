""" Modification to boofuzz """
from abc import ABC, abstractmethod
import math
import os
import socket
import struct

from .target_connection import TargetConnection


def _seconds_to_sockopt_format(seconds: float)-> struct:

    if os.name == "nt":
        return int(seconds * 1000)
    microseconds_per_second = 1000000
    whole_seconds = int(math.floor(seconds))
    whole_microseconds = int(math.floor((seconds % 1) * microseconds_per_second))

    return struct.pack("ll", whole_seconds, whole_microseconds)

class BaseSocketConnection(TargetConnection, ABC):

    def __init__(self, send_timeout:float, recv_timeout:float):
        self._send_timeout = send_timeout
        self._recv_timeout = recv_timeout
        self._host = None
        self._port = None

        self._sock = None

    def close(self)-> None:
        if self._sock:
            self._sock.close()

    @abstractmethod
    def open(self) -> None:
        if not self._sock: return
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, _seconds_to_sockopt_format(self._send_timeout))
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, _seconds_to_sockopt_format(self._recv_timeout))

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port



