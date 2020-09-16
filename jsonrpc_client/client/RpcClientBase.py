import json

from json import JSONEncoder
from collections import namedtuple
from typing import Tuple
from abc import ABC, abstractmethod

from jsonrpc_client.jsonrpc.JsonRpcMessages import Request, Notification, Response, make_response


class ClientException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class JsonRpcProtocolException(Exception):
    def __init__(self, message):
        #self.expression = expression
        self.message = message


class JsonCodec(object):
    def deserialize(self, resp: str):
        return make_response(resp)

    def serialize(self, req) -> bytes:
        return json.dumps(req).encode()


class RpcClientBase(ABC):
    def __init__(self):
        self.codec = JsonCodec()
        pass

    @abstractmethod
    def do_call(self, request: str) -> Response:
        pass

    def __validate_request(self, req) -> Tuple[bool, str]:
        return True, ''

    def __validate_response(self, request, response) -> Tuple[bool, str]:
        return True, ''

    def __deserialize(self, resp) -> Response:
        return self.codec.deserialize(resp)

    def __serialize(self, req) -> bytes:
        # If using a raw string as request, that's grand, just encode it and return. If it's an object like,
        # then we call the codec.
        return req.encode() if isinstance(req, str) else self.codec.serialize(req)

    def call(self, req) -> Response:
        Ok, Err = self.__validate_request(req)

        if Ok is False:
            raise JsonRpcProtocolException(Err)

        try:
            str_request = self.__serialize(req)
            str_response = self.do_call(str_request)

            if req.is_notification():
                # do not go any further, there is no response on notifications.
                print('sending none')
                return None

            resp = self.__deserialize(str_response.decode("utf-8"))

            Ok, Err = self.__validate_response(req, resp)
            if Ok is False:
                raise JsonRpcProtocolException(Err)

            return resp

        except Exception as ex:
            print(f'error {ex}')
            raise

        return None
