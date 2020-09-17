from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from ts_jsonrpc.jsonrpc.jsonrpc.JsonRpcMessages import Request, Response, Notification, make_response, BatchRequest


class ConfigCommandType(Enum):
    DEFAULTS = 1
    DESCRIBE = 2
    DIFF = 3
    GET = 4
    MATCH = 5
    RELOAD = 6
    SET = 7
    STATUS = 8


class StorageCommandType(Enum):
    STATUS = 1
    OFFLINE = 2


class MetricCommandType(Enum):
    CLEAR = 1
    DESCRIBE = 2
    GET = 3
    MATCH = 4
    MONITOR = 5
    ZERO = 6


class ServerCommandType(Enum):
    RPC = 1
    DRAIN = 2
    STOP_DRAIN = 3
    SHUTDOWN = 4
    RESTART = 5


class HostCommandType(Enum):
    UP = 1
    DOWN = 2
    STATUS = 3


class DataCommandType(Enum):
    JSON = 1
    YAML = 2
    FILE = 3

class PluginCommandType(Enum):
    MSG = 1


class RPCMessageBuilderBase(ABC):

    @abstractmethod
    def get_request(self):
        pass

    def get(self):
        return self.get_request()


class ConfigRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: ConfigCommandType, data: Any):
        self.cmdType = cmdType
        if not isinstance(data, bool):
            self.data = list(dict.fromkeys(data))

        if self.cmdType == ConfigCommandType.DEFAULTS or self.cmdType == ConfigCommandType.DIFF:
            self.req = Request.admin_config_get_all_records()
        elif self.cmdType == ConfigCommandType.GET or self.cmdType == ConfigCommandType.DESCRIBE:
            self.req = Request.admin_config_get_records(self.data)
        elif self.cmdType == ConfigCommandType.MATCH:
            self.req = Request.admin_config_get_records_regex(self.data)
        elif self.cmdType == ConfigCommandType.RELOAD:
            self.req = Request.admin_config_reload()
        elif self.cmdType == ConfigCommandType.SET:
            # support only one for now.
            self.req = Request.admin_config_set_records(
                [{'record_name': self.data[0], 'record_value': self.data[1]}])
        elif self.cmdType == ConfigCommandType.STATUS:
            self.data = [
                'proxy.process.version.server.long',
                'proxy.node.restarts.proxy.start_time',
                'proxy.node.config.reconfigure_time',
                'proxy.node.config.reconfigure_required',
                'proxy.node.config.restart_required.proxy']
            self.req = Request.admin_record_get_records_info(self.data)

        else:
            raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req


class StorageRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: ConfigCommandType, data: Any):
        self.cmdType = cmdType
        self.data = list(dict.fromkeys(data))

        if cmdType == StorageCommandType.OFFLINE:
            self.req = Request.admin_storage_set_device_offline(self.data)
        elif cmdType == StorageCommandType.STATUS:
            self.req = Request.admin_storage_get_device_status(self.data)
        else:
            raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req


class MetricRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: ConfigCommandType, data: Any):
        self.cmdType = cmdType
        if not isinstance(data, bool):
            self.data = list(dict.fromkeys(data))

        if self.cmdType == MetricCommandType.CLEAR:
            self.req = Request.admin_metric_get_all_records()
        elif self.cmdType == MetricCommandType.DESCRIBE:
            self.req = Request.admin_metric_get_records(self.data)
        elif self.cmdType == MetricCommandType.GET:
            self.req = Request.admin_metric_get_records(self.data)
        elif self.cmdType == MetricCommandType.MATCH:
            self.req = Request.admin_metric_get_records_regex(self.data)
        elif self.cmdType == MetricCommandType.MONITOR:
            self.req = Request.admin_metric_get_records(self.data)
        elif self.cmdType == MetricCommandType.ZERO:
            self.req = Request.admin_metric_clear(self.data)
        else:
            raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req


class PluginRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: ConfigCommandType, data: Any):
        self.cmdType = cmdType
        if not isinstance(data, bool):
            self.data = list(dict.fromkeys(data))
        raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req


class HostRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: ConfigCommandType, data: Any, opt):
        self.cmdType = cmdType
        self.data = list(dict.fromkeys(data))

        if self.cmdType == HostCommandType.UP:
            self.req = Request.admin_host_set_status(operation='up', host=self.data, reason=opt['reason'], time=opt['time'])
        elif self.cmdType == HostCommandType.DOWN:
            self.req = Request.admin_host_set_status(operation='down', host=self.data, reason=opt['reason'], time=opt['time'])
        elif self.cmdType == HostCommandType.STATUS:
            names = ["{}.{}".format('proxy.process.host_status', name) for name in self.data]
            self.req = Request.admin_metric_get_records(names)
        else:
            raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req


class ServerRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: ConfigCommandType, data: Any, opt):
        self.cmdType = cmdType
        self.opt = opt

        if self.cmdType == ServerCommandType.RPC:
            self.req = Request.show_registered_handlers()
        elif self.cmdType == ServerCommandType.STOP_DRAIN:
            self.req = Request.admin_server_stop_drain()
        elif self.cmdType == ServerCommandType.DRAIN:
            if 'N' in opt:
                self.req = Request.admin_server_start_drain(no_new_connections='yes')
            else:
                self.req = Request.admin_server_start_drain()
        elif self.cmdType == ServerCommandType.SHUTDOWN or self.cmdType == ServerCommandType.RESTART:
            self.req = Notification.admin_server_shutdown()
            print(self.req)
        else:
            raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req


class StringDataRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: DataCommandType, data: Any):
        self.cmdType = cmdType
        self.req = data

    def get_request(self):
        return self.req

class PluginRequest(RPCMessageBuilderBase):
    def __init__(self, cmdType: DataCommandType, data: Any):
        self.cmdType = cmdType
        self.data = data

        if self.cmdType == PluginCommandType.MSG:
            print(type(data))
            print(data)
            if 'tag' in self.data and 'data' in self.data:
                t = self.data['tag']
                d = self.data['data']
                self.req = Request.admin_plugin_send_basic_msg(tag=t, data=d)
            else:
                  raise Exception("Missing data")
        else:
            raise Exception(f"Command '{self.cmdType}' not available")

    def get_request(self):
        return self.req