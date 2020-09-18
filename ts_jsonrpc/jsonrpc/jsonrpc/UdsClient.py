import socket
import sys
import json
import pprint
import io

from typing import Tuple
from dataclasses import dataclass


from datetime import datetime
from ts_jsonrpc.jsonrpc.jsonrpc.RpcClientBase import RpcClientBase, ClientException


@dataclass
class Config:
    def __init__(self, path, timeOut=20, buffer=1024):
        self.path = path
        self.timeout = timeOut
        self.buffer = buffer

    path: str
    timeout: int
    buffer: int


class UdsClient(RpcClientBase):
    def __init__(self, conf: Config):
        super().__init__()
        self.config = conf

    # TODO: review and add ContextManager on this.
    def do_call(self, req: str) -> str:
        output = io.BytesIO()
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.settimeout(self.config.timeout)

            self.__connect()
            self.sock.sendall(req)
            amount_received = 0
            done = False
            while True:
                try:
                    data = self.sock.recv(self.config.buffer)
                except Exception as ex:
                    raise
                else:
                    if not data:
                        break

                    output.write(data)
                    # ugly, make this better, parse the json and check if it's valid.
                    # if we get a response in yaml, then validate the yaml lib.
                    if len(data) < self.config.buffer:
                        break

        except BaseException:
            raise
        finally:
            self.__disconnect()

        s = output.getvalue()
        output.close()
        return s

    def __connect(self):
        try:
            self.sock.connect(self.config.path)
        except socket.error as msg:
            raise ClientException('<>', msg.strerror)

    def __disconnect(self):
        try:
            if self.sock is not None:
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                except (socket.error, OSError, ValueError):
                    pass
                self.sock.close()
        except Exception as err:
            raise
