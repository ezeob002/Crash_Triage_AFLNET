import errno
import socket
import sys
from typing import Any, ByteString

from future.utils import raise_

from . import exception
from .base_socket_connection import BaseSocketConnection
from .ip_constants import *

""" Credit to BooFuzz"""
class TCPSocketConnection(BaseSocketConnection):

    def __init__(self,
                host:str,
                port:str,
                send_timeout:float=0.5,
                recv_timeout:float=0.5,
                server:bool=False):
        super(TCPSocketConnection, self).__init__(send_timeout, recv_timeout)
        self._host = host
        self._port = port
        self._server = server
        self._serverSock = None

    def close(self)-> None:
        super(TCPSocketConnection, self).close()
        if self._server: self._serverSock.close()

    def open(self) -> None:
        self._open_socket()
        self._connect_socket()

    def _open_socket(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._sock.settimeout(0.5)
        super(TCPSocketConnection, self).open()

    def _connect_socket(self):
        if self._server:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                self._sock.bind((self._host, self._port))
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    raise exception.FMIOutOfAvailableSockets()
                else:
                    raise

            self._serverSock = self._sock
            try:
                self._serverSock.listen(1)
                self._sock, addr = self._serverSock.accept()
            except socket.error as e:
                self.close()
                if e.errno in [errno.EAGAIN]:
                    raise exception.FMITargetConnectionFailedError(str(e))
                else:
                    raise
        else:
            try:
                self._sock.connect((self._host, self._port))
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    raise exception.FMIOutOfAvailableSockets()
                elif e.errno in [errno.ECONNREFUSED, errno.EINPROGRESS, errno.ETIMEDOUT]:
                    raise exception.FMITargetConnectionFailedError(str(e))
                else:
                    raise

    def recv(self, max_bytes: int = DEFAULT_MAX_RECV) -> Any:

        data = b""

        try:
            data = self._sock.recv(max_bytes)
        except socket.timeout:
            data = b""
        except socket.error as e:
            if e.errno == errno.ECONNABORTED:
                raise_(
                    exception.FMITargetConnectionAborted(socket_errno=e.errno, socket_errmsg=e.strerror),
                    None,
                    sys.exc_info()[2],
                )
            elif (e.errno == errno.ECONNRESET) or (e.errno == errno.ENETRESET) or (e.errno == errno.ETIMEDOUT):
                raise_(exception.FMITargetConnectionReset(), None, sys.exc_info()[2])
            elif e.errno == errno.EWOULDBLOCK:
                data = b""
            else:
                raise

        return data

    def send(self, data: Any) -> Any:

        num_sent = 0
        try:
            num_sent = self._sock.send(data)
        except socket.error as e:
            if e.errno == errno.ECONNABORTED:
                raise_(
                    exception.FMITargetConnectionAborted(socket_errno=e.errno, socket_errmsg=e.strerror),
                    None,
                    sys.exc_info()[2],
                )
            elif e.errno in [errno.ECONNRESET, errno.ENETRESET, errno.ETIMEDOUT, errno.EPIPE]:
                raise_(exception.FMITargetConnectionReset(), None, sys.exc_info()[2])
            else:
                raise

        return num_sent

    @property
    def info(self) -> None:
        return "{}:{}".format(self._host, self._port)
