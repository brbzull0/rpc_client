
import json
#import ruamel.yaml

from typing import Any
from ast import literal_eval
from io import StringIO
from enum import Enum
from abc import ABC, abstractmethod
from colorama import Fore, Back, Style
from collections import namedtuple
from ts_jsonrpc.cli.cli.TSUtils import *


def color(color, text, reset=True):
    return "{}{}{}".format(color, text, Style.RESET_ALL if reset else '')


def bright(text, reset=True):
    return color(Style.BRIGHT, text, reset)


selectedcolour = namedtuple('selectedcolour', ['ok', 'fail'])
sc = selectedcolour(ok=Fore.GREEN, fail=Fore.RED)
# sc = selectedcolour(ok='', fail='')
draw_box_char = "⏹"
# TODO: Add all the drawing unicode characters in variables which can be set to '' if
# the tool is flagged to show plain text.


def chain_print(lst, isError=False):
    output = StringIO()
    clr = sc.fail if isError else sc.ok
    if len(lst) == 1:
        output.write(f'{color(sc.ok, draw_box_char)} {lst[0]}\n')
        s = output.getvalue()
        output.close()
        return s
    space = ''
    output.write(f'{color(clr, "┌")} {lst[0]}\n')
    if len(lst) > 2:
        space = ' '
        # from 2nd till end-1
        output.write(f'{color(clr, "└┬──")} {lst[1]}\n')
        for x in lst[2:-1]:
            output.write(f'{color(clr, " ├──")} {x}\n')

    z = lst[-1]
    output.write(f'{space}{color(clr, "└──")} {z}\n')

    s = output.getvalue()
    output.close()
    return s


class FormattingType(Enum):
    LEGACY = 1
    RAW = 2
    JSON = 3
    YAML = 4
    PRETTY = 5
    RECORD = 6
    NONE = 7


class PrinterGenBase(ABC):
    def __init__(self, formattingType, **kwargs: Any):
        if kwargs:
            if 'req' in kwargs:
                self.req = kwargs['req']
            if 'resp' in kwargs:
                self.resp = kwargs['resp']

        self.formattingType = formattingType if formattingType is not FormattingType.NONE else FormattingType.PRETTY

        self.buff = StringIO()

    @abstractmethod
    def build_output_legacy(self, asRecord: bool):
        pass

    @abstractmethod
    def build_output_raw(self):
        pass

    def build_output_json(self):
        # req
        try:
            if self.req is not None:
                print(f"blah->{self.req}")
                s = json.dumps(literal_eval(
                    str(self.req)), indent=4, sort_keys=True)
                self.buff.write("-->\n")
                self.buff.write(s)
                self.buff.write('\n')
        except Exception as ex:
            self.buff.write("--> ' req cannot be render'")
        # resp
        try:
            if self.resp is not None:
                s = json.dumps(literal_eval(
                    str(self.resp)), indent=4, sort_keys=True)
                self.buff.write("< --\n")
                self.buff.write(s)
        except Exception as ex:
            self.buff.write("<-- ' resp cannot be render'")

    def build_output_yaml(self):
        print("before printing yaml")
        #d = self.resp.get_as_dict()
        # a = yaml.dump(yaml.load(d, yaml.SafeLoader))
        # print(type(a))
        # print(ruamel.yaml.round_trip_load("{'a"))
        # self.buff.write(yaml.dump(yaml.load(d), default_flow_style=False))
        # self.buff.write('\n')
        # self.buff.write(yaml.dump(yaml.load(d)))
        print("after printing yaml")

    def build_output_pretty(self):
        pass

    @abstractmethod
    def build_output_mutted(self):
        pass

    def __generate_output(self):
        print(f"Formatting type {self.formattingType}")
        if self.formattingType is FormattingType.LEGACY:
            self.build_output_legacy(False)
        elif self.formattingType is FormattingType.RECORD:
            self.build_output_legacy(True)
        elif self.formattingType is FormattingType.RAW:
            self.build_output_raw()
        elif self.formattingType is FormattingType.JSON:
            self.build_output_json()
        elif self.formattingType is FormattingType.YAML:
            self.build_output_yaml()
        elif self.formattingType is FormattingType.PRETTY:
            self.build_output_pretty()
        else:
            self.build_output_mutted()

    def __str__(self):
        try:
            self.__generate_output()
            s = self.buff.getvalue()
            self.buff.close()
            return s
        except BaseException:
            return ''


class RecordPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        for record in self.resp.result:
            if asRecord:
                self.buff.write(
                    "{} {} {} {}\n".format(
                        class_to_string(
                            record['record_class']),
                        record['name'],
                        type_to_string(
                            record['record_type']),
                        record['current_value']))
            else:
                self.buff.write("{}: {}\n".format(
                    record['name'], record['current_value']))

    def build_output_pretty(self):
        for record in self.resp.result:
            self.buff.write(
                f'{color(sc.ok, draw_box_char)} {record["name"]}: {record["current_value"]}\n')

    def build_output_mutted(self):
        pass

    def build_output_raw(self):
        self.buff.write(str(self.resp.result))


class ConfigDescribePrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        for record in self.resp.result:
            self.buff.write("{:16s}: {}\n".format('Name', record['name']))
            self.buff.write("{:16s}: {}\n".format(
                'Current Value', record['current_value']))
            self.buff.write("{:16s}: {}\n".format(
                'Default Value', record['default_value']))
            self.buff.write("{:16s}: {}\n".format(
                'Record Type', type_to_string(record['record_type'])))
            self.buff.write("{:16s}: {}\n".format(
                'Access Control', access_control_to_string(record['access'])))
            self.buff.write("{:16s}: {}\n".format(
                'Update Type', update_type_to_string(record['update_type'])))
            self.buff.write("{:16s}: {}\n".format(
                'Update Status', record['update_status']))
            self.buff.write("{:16s}: {}\n".format(
                'Source', source_to_string(record['source'])))
            self.buff.write("{:16s}: {}\n".format(
                'Overridable', record['overridable']))
            self.buff.write("{:16s}: {}\n".format(
                'Syntax Check', syntax_check_to_string(record['syntax_check'])))
            self.buff.write("{:16s}: {}\n".format(
                'Version', record['version']))
            self.buff.write("{:16s}: {}\n".format('Order', record['order']))
            self.buff.write("{:16s}: {}\n".format(
                'Raw Stat Block', record['raw_stat_block']))

    def build_output_pretty(self):
        for record in self.resp.result:
            self.buff.write(chain_print([f'{bright(record["name"])}',
                                         f'{"Current Value:":16} {bright(record["current_value"])}',
                                         f'{"Default Value:":16} {bright(record["default_value"])}',
                                         f'{"Record Type:":16} {bright(type_to_string(record["record_type"]))}',
                                         f'{"Access Control:":16} {bright(access_control_to_string(record["access"]))}',
                                         f'{"Update Type:":16} {bright(update_type_to_string(record["update_type"]))}',
                                         f'{"Update Status:":16} {bright(record["update_status"])}',
                                         f'{"Source:":16} {bright(source_to_string(record["source"]))}',
                                         f'{"Overridable:":16} {bright(record["overridable"])}',
                                         f'{"Syntax Check:":16} {bright(syntax_check_to_string(record["syntax_check"]))}',
                                         f'{"Version:":16} {bright(record["version"])}',
                                         f'{"Order:":16} {bright(record["order"])}',
                                         f'{"Raw Stat Block:":16} {bright(record["raw_stat_block"])}']))

    def build_output_mutted(self):
        pass

    def build_output_raw(self):
        self.buff.write(str(self.resp.result))


class ConfigDiffPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        for record in self.resp.result:
            hashChanged = record['current_value'] != record['default_value']
            if hashChanged:
                if asRecord:
                    self.buff.write(
                        "{} {} {} {} # default: {}\n".format(
                            class_to_string(
                                record['record_class']),
                            record['name'],
                            type_to_string(
                                record['record_type']),
                            record['current_value'],
                            record['default_value']))
                else:
                    self.buff.write("{} has changed\n".format(record['name']))
                    self.buff.write("{:>8}{:16s} {}\n".format(
                        "", "Current Value:", record['current_value']))
                    self.buff.write("{:>8}{:16s} {}\n".format(
                        "", "Default Value:", record['default_value']))

    def build_output_pretty(self):
        for record in self.resp.result:
            hashChanged = record['current_value'] != record['default_value']
            if hashChanged:
                self.buff.write(chain_print([f'{bright(record["name"])} has changed',
                                             f'Current Value:{str(""):4}{record["current_value"]}',
                                             f'Default Value:{str(""):4}{record["default_value"]}']))

    def build_output_raw(self):
        pass

    def build_output_mutted(self):
        pass


class SuccessPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        self.buff.write("Ok")

    def build_output_pretty(self):
        self.buff.write("Ok")

    def build_output_raw(self):
        self.buff.write(str(self.resp.result))

    def build_output_mutted(self):
        pass


class GenericPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        pass

    def build_output_pretty(self):
        pass

    def build_output_raw(self):
        pass

    def build_output_mutted(self):
        pass


class RpcPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        pass

    def build_output_pretty(self):
        if 'methods' in self.resp.result:
            lst = ['Methods']
            for m in self.resp.result['methods']:
                lst.append(f' {bright(m)}')
            self.buff.write(chain_print(lst))
        else:
            self.buff.write(
                f'{color(sc.ok, draw_box_char)} No registered methods.\n')

        if 'notifications' in self.resp.result:
            lst = ['Notifications']
            for m in self.resp.result['notifications']:
                lst.append(f' {bright(m)}')
            self.buff.write(chain_print(lst))
        else:
            self.buff.write(
                f'{color(sc.ok, draw_box_char)} No registered notifications.\n')

    def build_output_raw(self):
        self.buff.write(str(self.resp.result))

    def build_output_mutted(self):
        pass


class ConfigSetPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        pass

    def build_output_pretty(self):
        self.buff.write(chain_print([f'{bright(self.resp.result["record_name"])}',
                                     f'{"New Value:":16} {bright(self.resp.result["new_value"])}',
                                     f'{"Update Status:":16} {bright(update_type_to_string(self.resp.result["update_status"]))}']))

    def build_output_raw(self):
        self.buff.write(str(self.resp.result))

    def build_output_mutted(self):
        pass


class StoragePrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)
        if kwargs and 'opt' in kwargs:
            self.opt = kwargs['opt']

    def build_output_legacy(self, asRecord: bool):
        self.buff.write("Ok")

    def build_output_pretty(self):
        if 'offline' in self.opt:
            for d in self.resp.result:
                self.buff.write(
                    f'{d["device"]} - online device left: {d["has_online_storage_left"]}\n')
        elif 'status' in self.opt:
            for disk in self.resp.result:
                self.buff.write(chain_print([f'{bright(disk["path"])}',
                                             f'{"Error count:":16} {disk["error_count"]}',
                                             f'{"Status:":16} {disk["status"]}']))
        else:
            pass

    def build_output_raw(self):
        self.buff.write(str(self.resp.result))

    def build_output_mutted(self):
        pass


class ErrorPrinterGen(PrinterGenBase):
    def __init__(self, formattingType, **kwargs: Any):
        super().__init__(formattingType, **kwargs)

    def build_output_legacy(self, asRecord: bool):
        self.buff.write(f"{self.resp.error['code']}")
        if 'data' in self.resp.error:
            for err in self.resp.error['data']:
                self.buff.write(f",{err['code']}")
        self.buff.write(f": {self.resp.error['message']}\n")

    def build_output_pretty(self):
        self.buff.write("Error received from the server\n")
        lst = []
        lst.append(
            f'Code: {bright(self.resp.error["code"])} - Description: {bright(self.resp.error["message"])}')

        if 'data' in self.resp.error:
            lst.append('Additional error information')
            idx = 1
            for e in self.resp.error['data']:
                lst.append(
                    f'Code: {bright(e["code"])}, Message: {bright(e["message"])}')
        isError = True
        self.buff.write(chain_print(lst, isError))
        self.buff.write("\n")

    def build_output_raw(self):
        self.buff.write(str(self.resp.error))

    def build_output_mutted(self):
        pass
