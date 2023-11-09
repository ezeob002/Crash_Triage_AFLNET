from abc import ABC, abstractmethod
from .ip_constants import DEFAULT_MAX_RECV
from typing import Any

class TargetConnection(ABC):

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def open(self)-> None:
        pass

    @abstractmethod
    def recv(self, max_bytes: int = DEFAULT_MAX_RECV) -> Any:
        pass


    @abstractmethod
    def send(self, data: Any) -> Any:
        pass

    @property
    @abstractmethod
    def info(self) -> str:
        pass


    def recv_all(self, max_bytes: int=DEFAULT_MAX_RECV)-> Any:

        chunk = self.recv(max_bytes)
        data = chunk
        while chunk and len(data) < max_bytes:
            chunk = self.recv(max_bytes - len(data))
            data += chunk
        return data




