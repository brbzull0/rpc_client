import json

from json import JSONEncoder
from collections import namedtuple
from typing import Tuple
from abc import ABC, abstractmethod

from ts_jsonrpc.jsonrpc.jsonrpc.JsonRpcMessages import Request, Notification, Response, make_response


class ClientException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
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
    def do_call(self, request: str) -> str:
        pass

    def __validate_request(self, req) -> Tuple[bool, str]:
        return True, ''

    def __validate_response(self, request, response) -> Tuple[bool, str]:
        # add validation if the request wasn't a notification and we get nothing back.
        return True, ''

    def __deserialize(self, resp) -> Response:
        return self.codec.deserialize(resp)

    def __serialize(self, req) -> bytes:
        # If using a raw string as request, that's grand, just encode it and return. If it's an object like,
        # then we call the codec.
        return req.encode() if isinstance(req, str) else self.codec.serialize(req)

    def __is_notification(self, req):
        if isinstance(req, str):
            try:
                json_req = json.loads(req)
                if 'id' in json_req:
                    return False
                else:
                    return True
            except Exception as e:
                raise
        else:
            return req.is_notification()

    def call(self, req) -> Response:
        Ok, Err = self.__validate_request(req)

        if Ok is False:
            raise Exception(Err)

        try:
            str_request = self.__serialize(req)
            str_response = self.do_call(str_request)
            print(f' response: {str_response}')
            if str_response == '' and self.__is_notification(req) == False:
                raise Exception("We haven't got a response when it was expected.")

            if self.__is_notification(req):
                # no need to move further on this.
                return None

            resp = self.__deserialize(str_response.decode("utf-8"))

            Ok, Err = self.__validate_response(req, resp)
            if Ok is False:
                raise Exception(Err)

            return resp

        except Exception as ex:
            raise

        return None
