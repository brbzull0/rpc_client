import os
from enum import Enum

from typing import Tuple, Union, Any

from ts_jsonrpc.jsonrpc.jsonrpc.UdsClient import UdsClient, Config
from ts_jsonrpc.jsonrpc.jsonrpc.RpcClientBase import RpcClientBase
from ts_jsonrpc.jsonrpc.jsonrpc.JsonRpcMessages import Request, Notification, Response

from ts_jsonrpc.cli.cli.Printer import ConfigDescribePrinterGen, ErrorPrinterGen, FormattingType, RecordPrinterGen, SuccessPrinterGen, ConfigDiffPrinterGen, ConfigSetPrinterGen, RpcPrinterGen, GenericPrinterGen
from ts_jsonrpc.cli.cli.Request import ConfigRequest, ServerRequest, StorageRequest, MetricRequest, HostRequest, StringDataRequest, RPCMessageBuilderBase, ConfigCommandType, StorageCommandType, MetricCommandType, ServerCommandType, HostCommandType, DataCommandType, PluginCommandType, PluginRequest


ft_dict = {'legacy': FormattingType.LEGACY,
           'raw': FormattingType.RAW,
           'json': FormattingType.JSON,
           'yaml': FormattingType.YAML,
           'pretty': FormattingType.PRETTY,
           'records': FormattingType.RECORD}


def make_config_printer(ft, args, req, response):
    if args.records:
        ft = FormattingType.RECORD  # not very nice

    if args.describe:
        return ConfigDescribePrinterGen(ft, req=req, resp=response)
    elif args.diff:
        return ConfigDiffPrinterGen(ft, req=req, resp=response)
    elif args.set:
        return ConfigSetPrinterGen(ft, req=req, resp=response)
    else:
        return RecordPrinterGen(ft, req=req, resp=response)


def make_storage_printer(ft, args, req, response):
    opt = []
    if args.status:
        opt.append('status')
    elif args.offline:
        opt.append('offline')

    return StoragePrinterGen(ft, req=response, opt=opt)


def make_server_printer(ft, args, req, response):
    if args.rpc:
        return RpcPrinterGen(ft, req=req, resp=response)
    else:
        return GenericPrinterGen(ft, req=req, resp=response)


def make_printer(args, **kwargs: Any):
    req = None
    response = None

    if kwargs:
        if 'req' in kwargs:
            req = kwargs['req']
        if 'resp' in kwargs:
            response = kwargs['resp']

    ft = ft_dict[args.formatting]

    # if this was a notification, response will not hold any value, so send the generic printer
    # back, which will not display anything.
    if response is None:
        return GenericPrinterGen(ft, req=req)

    if response.is_error():
        return ErrorPrinterGen(ft, req=req, resp=response)
    elif response.is_only_success():
        return SuccessPrinterGen(ft, req=req, resp=response)
    elif response.is_Ok():
        if args.action == 'config':
            return make_config_printer(ft, args, req, response)
        elif args.action == 'metric':
            return RecordPrinterGen(ft, resp=response)
        elif args.action == 'storage':
            return make_storage_printer(ft, args, req, response)
        elif args.action == 'host':
            return RecordPrinterGen(ft, resp=response)
        elif args.action == 'server':
            return make_server_printer(ft, args, req, response)
        elif args.action == 'data':
            return GenericPrinterGen(ft, req=req, resp=response)
        elif args.action == 'plugin':
            return GenericPrinterGen(ft, req=req, resp=response)
        else:
            return GenericPrinterGen(ft)
    else:
        return GenericPrinterGen(ft)


def config_param_to_enum(args):
    if args.describe:
        return ConfigCommandType.DESCRIBE, args.describe
    elif args.diff:
        return ConfigCommandType.DIFF, args.diff
    elif args.defaults:
        return ConfigCommandType.DEFAULTS, args.defaults
    elif args.get:
        return ConfigCommandType.GET, args.get
    elif args.match:
        return ConfigCommandType.MATCH, args.match
    elif args.reload:
        return ConfigCommandType.RELOAD, args.reload
    elif args.set:
        return ConfigCommandType.SET, args.set
    elif args.status:
        return ConfigCommandType.STATUS, args.status
    else:
        pass


def storage_param_to_enum(args):
    if args.offline:
        return StorageCommandType.OFFLINE, args.offline
    elif args.status:
        return StorageCommandType.STATUS, args.status
    else:
        pass


def metric_param_to_enum(args):
    if args.clear:
        return MetricCommandType.CLEAR, args.clear
    elif args.describe:
        return MetricCommandType.DESCRIBE, args.describe
    elif args.get:
        return MetricCommandType.GET, args.get
    elif args.match:
        return MetricCommandType.MATCH, args.match
    elif args.monitor:
        return MetricCommandType.MONITOR, args.monitor
    elif args.zero:
        return MetricCommandType.ZERO, args.zero
    else:
        pass


def server_param_to_enum(args):
    if args.rpc:
        return ServerCommandType.RPC, None, None
    elif args.drain:
        return ServerCommandType.DRAIN, None, args.drain
    elif args.stop_drain:
        return ServerCommandType.STOP_DRAIN, None, None
    elif args.shutdown:
        return ServerCommandType.SHUTDOWN, None, None
    elif args.restart:
        return ServerCommandType.RESTART, None, None
    else:
        pass


def host_param_to_enum(args):
    opt = {}
    if args.reason:
        opt['reason'] = args.reason
    if args.time:
        opt['time'] = args.time

    if args.up:
        return HostCommandType.UP, args.up, opt
    elif args.down:
        return HostCommandType.DOWN, args.down, opt
    elif args.status:
        return HostCommandType.STATUS, args.status, None
    else:
        pass


def data_from_param_action(args):
    if args.json:
        return DataCommandType.JSON, args.json
    elif args.file:
        try:
            file = open(args.file, "r", encoding="utf-8")
            data = file.read()
            return DataCommandType.FILE, data
        except Exception as ex:
            raise ex


def plugin_data_from_action(args):
    if args.msg:
        data = {'tag': args.msg[0], 'data': args.msg[1]}
        return PluginCommandType.MSG, data
    else:
        None, None


def make_call(args):
    # request
    if args.action == 'config':
        cmdType, data = config_param_to_enum(args)
        return Call(ConfigRequest(cmdType, data))
    elif args.action == 'storage':
        cmdType, data = storage_param_to_enum(args)
        return Call(StorageRequest(cmdType, data))
    elif args.action == 'metric':
        cmdType, data = metric_param_to_enum(args)
        return Call(MetricRequest(cmdType, data))
    elif args.action == 'host':
        cmdType, data, opt = host_param_to_enum(args)
        return Call(HostRequest(cmdType, data, opt))
    elif args.action == 'server':
        cmdType, data, opt = server_param_to_enum(args)
        return Call(ServerRequest(cmdType, data, opt))
    elif args.action == 'plugin':
        cmdType, data = plugin_data_from_action(args)
        return Call(PluginRequest(cmdType, data))
    elif args.action == 'data':
        cmdType, data = data_from_param_action(args)
        return Call(StringDataRequest(cmdType, data))
    else:
        pass


class Call:
    def __init__(self, request: RPCMessageBuilderBase):
        # We use UDS for now.
        path = os.getenv('JSONRPC20_SOCK_PATH', '/tmp/jsonrpc20.sock')
        # define a config file for this??
        self.conf = Config(path, 20, 1013)
        self.jsonrpcRequest = request.get()

    def execute(self) -> Tuple[Union[Request, Notification], Response]:
        c = UdsClient(self.conf)

        # Call client and make the call.
        jsonRpcResponse = c.call(self.jsonrpcRequest)
        # if notification, response will be None
        return self.jsonrpcRequest, jsonRpcResponse


def handle_command(args):
    try:
        call = make_call(args)

        request, response = call.execute()

        if args.verbose:
            if request is not None:
                print(f"--> {request}")
            if response is not None:
                print(f"<-- {response}")

        printer = make_printer(args, req=request, resp=response)
        # display output
        print(printer)

    except Exception as ex:
        raise
