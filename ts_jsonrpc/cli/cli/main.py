#from .Commands import run_command
import sys
import argparse
import sys
import traceback
from colorama import Fore, Back, Style
from setuptools import setup, find_packages
from distutils.util import convert_path

from ts_jsonrpc.cli.cli.CmdSender import handle_command
from ts_jsonrpc.cli.cli.Printer import FormattingType

parser = argparse.ArgumentParser(description="{}Apache Traffic Server RPC TEST tool{}".format(Style.BRIGHT, Style.RESET_ALL))


def configuration_handler(args):
    if args.defaults or args.describe or args.diff or args.get or args.match or args.status or args.set or args.reload:
        handle_command(args)
    else:
        parser.print_help()


def metric_handler(args):
    if args.describe or args.get or args.match or args.monitor or args.clear or args.zero:
        handle_command(args)
    else:
        parser.print_help()


def print_not_implemented():
    print("Option not yet implemented.")


def host_handler(args):
    if args.up or args.down or args.status:
        handle_command(args)
    else:
        print_not_implemented()


def plugin_handler(args):
    if args.msg:
        handle_command(args)


def server_handler(args):
    if args.rpc or args.drain or args.stop_drain or args.restart or args.shutdown:
        handle_command(args)
    else:
        print_not_implemented()


def storage_handler(args):
    if args.offline or args.status:
        handle_command(args)
    else:
        print_not_implemented()


def rpc_handler(args):
    if args.showhandlers:
        handle_command(args)


def data_handler(args):
    if args.json or args.file:
        handle_command(args)


def main():

    parser.add_argument('-v', '--version', action='version', version='alpha-0.0.1', help="Show current version")
    parser.add_argument('-d', '--verbose', action='store_true', help="Display raw request and response message")
    parser.add_argument('-r', '--repeat', nargs='?', metavar='count', help="Repeat the same command N times")
    parser.add_argument('-s', '--sim', action='store_true', help="Show json, don't send the message[not implemented]")
    parser.add_argument(
        '-f',
        '--formatting',
        nargs='?',
        choices=[
            'legacy',
            'raw',
            'json',
            'yaml',
            'pretty'],
        default='pretty',
        type=str, help="Output formatting options")

    subparsers = parser.add_subparsers(title='Commands', description='Basic interaction command to talk with ATS', dest='action')

    data_parser = subparsers.add_parser('data', help='Accept raw json and yaml as request')
    mxg_data = data_parser.add_mutually_exclusive_group(required=False)
    mxg_data.add_argument('--json', metavar='json msg', nargs='?', help='Send raw json request')
    mxg_data.add_argument('--file', metavar='File name', nargs='?', help='Send raw data, either json or yaml')
    mxg_data.set_defaults(func=data_handler)

    # configurations
    config_parser = subparsers.add_parser('config', aliases=['c'], help='Manipulate configuration records')
    config_parser.add_argument('--records', action='store_true', help='Emit output in records.config format')
    mxg_config = config_parser.add_mutually_exclusive_group(required=True)
    mxg_config.add_argument('--defaults', action='store_true', help='Show default information configuration values')
    mxg_config.add_argument('--describe', nargs='+', metavar='var_name',
                            help='Show detailed information about configuration values')
    mxg_config.add_argument('--diff', action='store_true', help='Show non-default configuration values')
    mxg_config.add_argument('--get', nargs='+', metavar='var_name', help='Get one or more configuration values')
    mxg_config.add_argument('--match', nargs='+', metavar='regex', help='Get configuration matching a regular expression')
    mxg_config.add_argument('--reload', action='store_true', help='Request a configuration reload')
    mxg_config.add_argument('--set', nargs=2, metavar='var_name', help='Set a configuration value')
    mxg_config.add_argument('--status', action='store_true', help='Check the configuration status')
    mxg_config.set_defaults(func=configuration_handler)

    # host
    host_parser = subparsers.add_parser(
        'host', aliases=['h'], help='Interact with host status')
    host_parser.add_argument('--reason', nargs='?', choices=[
        'active',
        'local',
        'manual'],
        default='manual', type=str)
    host_parser.add_argument('--time', nargs='?', metavar='secs', help='Time in seconds', default='0')
    mxg_host = host_parser.add_mutually_exclusive_group(required=True)
    mxg_host.add_argument('--down', nargs='+', metavar='host', help='Set down one or more host(s)')
    mxg_host.add_argument('--up', nargs='+', help='Set up one or more host(s)')
    mxg_host.add_argument('--status', nargs='+', metavar='host name', help='Get one or more host statuses')
    mxg_host.set_defaults(func=host_handler)

    # metrics
    metric_parser = subparsers.add_parser('metric', aliases=['m'], help='Manipulate performance metrics')
    mxg_metric = metric_parser.add_mutually_exclusive_group(required=True)
    mxg_metric.add_argument('--clear', action='store_true', help='Clear all metric values')
    mxg_metric.add_argument('--describe', nargs='+', help='defaults help')
    mxg_metric.add_argument('--get', nargs='+', help='defaults help')
    mxg_metric.add_argument('--match', nargs='+', help='defaults help')
    mxg_metric.add_argument('--monitor', nargs='+', help='defaults help')
    mxg_metric.add_argument('--zero', nargs='+', help='Clear metric')
    mxg_metric.set_defaults(func=metric_handler)

    # Plugin
    plugin_parser = subparsers.add_parser('plugin', aliases=['p'], help='Interact with plugins')
    mxg_plugin = plugin_parser.add_mutually_exclusive_group(required=True)
    mxg_plugin.add_argument('--msg', nargs=2, help='Send message to plugins - a TAG and the message DATA')
    mxg_plugin.set_defaults(func=plugin_handler)

    # Server
    server_parser = subparsers.add_parser('server', aliases=['s'], help='Stop, restart and examine the server ????')
    mxg_server = server_parser.add_mutually_exclusive_group(required=True)
    mxg_server.add_argument('--rpc', nargs='?', choices=['api'], help='RPC server handling')
    mxg_server.add_argument('--drain', nargs='?', choices=['N', 'O'], const='O', help='RPC server handling')
    mxg_server.add_argument('--stop-drain', action='store_true', help='RPC server handling')
    mxg_server.add_argument('--shutdown', action='store_true', help='Mark the server for shutdown')
    mxg_server.add_argument('--restart', action='store_true', help='Mark the server for restart')

    ddp = server_parser.add_subparsers(title='server2')
    drain_parser = ddp.add_parser('--drain', help='some help')
    drain_parser.add_argument('-N', help='help n')
    drain_parser.add_argument('-U', help='help u')
    shutdown_parser = ddp.add_parser('--restart')
    shutdown_parser.add_argument('-A')
    shutdown_parser.add_argument('-B')

    mxg_server.set_defaults(func=server_handler)

    # Storage
    storage_parser = subparsers.add_parser('storage', aliases=['st'], help='Manipulate cache storage')
    mxg_storage = storage_parser.add_mutually_exclusive_group(required=True)
    mxg_storage.add_argument('--offline', nargs='+', help='Set devices offline')
    mxg_storage.add_argument('--status', nargs='+', help='Show device status')
    mxg_storage.set_defaults(func=storage_handler)

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.error("Too few arguments")
    try:
        func(args)
    except Exception as e:
        print("Something went wrong: {}".format(e))
        # traceback.print_exc(file=sys.stdout)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('bye')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
