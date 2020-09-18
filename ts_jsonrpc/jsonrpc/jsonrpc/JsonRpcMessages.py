from typing import List, Callable, Any, Union
from dataclasses import dataclass
from collections import OrderedDict
import json
import uuid


class BaseRequestType(type):
    # TODO: Add some expl.
    def __getattr__(cls: Callable, name: str) -> Callable:
        def attr_handler(*args: Any, **kwargs: Any) -> "Request":
            return cls(name, *args, **kwargs)
        return attr_handler


class Notification(dict, metaclass=BaseRequestType):
    def __init__(self, method: str, *args: Any, **kwargs: Any):
        super(Notification, self).__init__(jsonrpc='2.0', method=method)
        if args and kwargs:
            plist = list(args)
            plist.append(kwargs)
            self.update(params=plist)
        elif args:
            if isinstance(args, tuple):
                # fix this. this is to avoid having params=[[values] which seems invalid. Double check this as [[],[]] would be ok.
                self.update(params=args[0])
            else:
                self.update(params=list(args))
        elif kwargs:
            self.update(params=kwargs)

    # Allow using the dict item as attribute.
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def is_notification(self):
        return True

    def __str__(self) -> str:
        return json.dumps(self)


class Request(Notification):
    def __init__(self, method: str, *args: Any, **kwargs: Any):
        if 'id' in kwargs:
            self.update(id=kwargs.pop('id'))  # avoid duplicated
        else:
            self.update(id=str(uuid.uuid1()))

        super(Request, self).__init__(method, *args, **kwargs)

    def is_notification(self):
        return False


class BatchRequest(list):
    def __init__(self, *args: Union[Request, Notification]):
        for r in args:
            self.append(r)

    def add_request(self, req: Union[Request, Notification]):
        self.append(req)

    def __str__(self) -> str:
        return json.dumps(self)


class Response(dict):
    def __init__(self, **kwargs):

        if 'text' in kwargs:
            self.__dict__ = json.loads(kwargs['text'])
        elif 'json' in kwargs:
            self.__dict__ = kwargs['json']

    def is_error(self) -> bool:
        if 'error' in self.__dict__:
            return True
        return False

    def is_only_success(self) -> bool:
        if self.is_Ok() and self.result == 'success':
            return True

        return False

    def is_Ok(self) -> bool:
        return not self.is_error()

    def get_as_dict(self):
        return self.__dict__

    def __str__(self) -> str:
        return json.dumps(self.__dict__)


def make_response(text):
    if text == '':
        return None

    s = json.loads(text)
    if isinstance(s, dict):
        return Response(json=s)
    elif isinstance(s, list):
        batch = []
        for r in s:
            batch.append(Response(json=r))
        return batch
