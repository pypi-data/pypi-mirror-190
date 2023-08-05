#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : entry.py 
@time    : 2022/12/18
@site    :  
@software: PyCharm 

              ,----------------,              ,---------,
         ,-----------------------,          ,"        ,"|
       ,"                      ,"|        ,"        ,"  |
      +-----------------------+  |      ,"        ,"    |
      |  .-----------------.  |  |     +---------+      |
      |  |                 |  |  |     | -==----'|      |
      |  | $ sudo rm -rf / |  |  |     |         |      |
      |  |                 |  |  |/----|`---=    |      |
      |  |                 |  |  |   ,/|==== ooo |      ;
      |  |                 |  |  |  // |(((( [33]|    ,"
      |  `-----------------'  |," .;'| |((((     |  ,"
      +-----------------------+  ;;  | |         |,"
         /_)______________(_/  //'   | +---------+
    ___________________________/___  `,
   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""

import abc
import functools
import logging
import os
import sys
import textwrap
import traceback
from abc import ABC
from argparse import ArgumentParser, Action, SUPPRESS, RawDescriptionHelpFormatter
from typing import Tuple, Type, Optional

from rich import get_console
from rich.prompt import IntPrompt
from rich.table import Table

from .._environ import environ
from .._logging import LogHandler, get_logger
from ..decorator import cached_property
from ..utils import ignore_error
from ..version import __version__, __description__


class Command(abc.ABC):
    logger: logging.Logger = property(lambda self: self._logger)
    description: str = cached_property(lambda self: textwrap.dedent((self.__doc__ or "").strip()))
    argument_parser: ArgumentParser = cached_property(lambda self: self._create_argument_parser())
    known_errors: Tuple[Type[BaseException]] = property(lambda self: self._known_errors)

    def main(self, *args, **kwargs) -> None:
        try:
            self._main_init()
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",
                datefmt="[%X]",
                handlers=[LogHandler()]
            )
            exit(self(*args, **kwargs))
        finally:
            self._main_deinit()

    def _main_init(self):
        pass

    def _main_deinit(self):
        pass

    @property
    def _logger(self) -> logging.Logger:
        return get_logger()

    @property
    def _known_errors(self) -> Tuple[Type[BaseException]]:
        return tuple()

    @abc.abstractmethod
    def _add_arguments(self, parser: ArgumentParser) -> None:
        pass

    @abc.abstractmethod
    def _run(self, args: [str]) -> Optional[int]:
        pass

    def __call__(self, args: [str] = None) -> int:
        try:
            args = args if args is not None else sys.argv[1:]
            exit_code = self._run(args) or 0

        except SystemExit as e:
            exit_code = e.code

        except (KeyboardInterrupt, EOFError, *self.known_errors) as e:
            exit_code = 1
            error_type, error_message = e.__class__.__name__, str(e).strip()
            self.logger.error(f"{error_type}: {error_message}" if error_message else error_type)

        except:
            exit_code = 1
            if environ.debug:
                console = get_console()
                console.print_exception(show_locals=True)
            else:
                self.logger.error(traceback.format_exc())

        return exit_code

    def _create_argument_parser(self):

        description = self.description.strip()
        if description:
            description += os.linesep + os.linesep
        description += __description__

        parser = ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            description=description,
            conflict_handler="resolve"
        )
        self._add_base_arguments(parser)
        self._add_arguments(parser)

        return parser

    def _add_base_arguments(self, parser: ArgumentParser):

        class VerboseAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                environ.logger.setLevel(logging.DEBUG)

        class DebugAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                environ.debug = True
                environ.logger.setLevel(logging.DEBUG)

        class BooleanOptionalAction(Action):

            def format_usage(self):
                return ' | '.join(self.option_strings)

        class LogTimeAction(BooleanOptionalAction):

            def __call__(self, parser, namespace, values, option_string=None):
                if option_string in self.option_strings:
                    environ.show_log_time = not option_string.startswith("--no-")

        class LogLevelAction(BooleanOptionalAction):

            def __call__(self, parser, namespace, values, option_string=None):
                if option_string in self.option_strings:
                    environ.show_log_level = not option_string.startswith("--no-")

        parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

        group = parser.add_argument_group(title="log arguments")
        group.add_argument("--verbose", action=VerboseAction, nargs=0, const=True, dest=SUPPRESS,
                           help="increase log verbosity")
        group.add_argument("--debug", action=DebugAction, nargs=0, const=True, dest=SUPPRESS,
                           help="enable debug mode and increase log verbosity")

        if LogHandler.get_instance():
            group.add_argument("--time", "--no-time", action=LogTimeAction, nargs=0, dest=SUPPRESS,
                               help="show log time")
            group.add_argument("--level", "--no-level", action=LogLevelAction, nargs=0, dest=SUPPRESS,
                               help="show log level")


class AndroidCommand(Command, ABC):

    @property
    def _known_errors(self) -> Tuple[Type[BaseException]]:
        from linktools.android import AdbError
        return AdbError,

    def _add_base_arguments(self, parser: ArgumentParser):
        super()._add_base_arguments(parser)

        from linktools.android import Adb, Device, AdbError
        cache_path = environ.resource.get_temp_path("cache", "device", "android", create_parent=True)

        def parse_handler(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                device = fn(*args, **kwargs)
                if device is not None:
                    with open(cache_path, "wt+") as fd:
                        fd.write(device.id)
                return device

            return wrapper

        @parse_handler
        def parse_device():
            devices = Adb.devices(alive=True)
            if len(devices) == 0:
                raise AdbError("no devices/emulators found")

            if len(devices) == 1:
                return devices[0]

            table = Table(show_lines=True)
            table.add_column("Index", justify="right", style="cyan", no_wrap=True)
            table.add_column("Serial", style="magenta")
            table.add_column("Model", style="magenta")

            offset = 1
            for i in range(len(devices)):
                table.add_row(
                    str(i + offset),
                    devices[i].id,
                    ignore_error(lambda: devices[i].get_prop("ro.product.model", timeout=1)) or "",
                )

            console = get_console()
            console.print(table)

            prompt = f"More than one device/emulator. {os.linesep}" \
                     f"Enter device index"
            choices = [str(i) for i in range(offset, len(devices) + offset, 1)]
            index = IntPrompt.ask(prompt, choices=choices, default=offset, console=console)

            return devices[index - offset]

        class SerialAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    return Device(str(values))

                setattr(namespace, self.dest, wrapper)

        class DeviceAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    return Device(Adb.exec("-d", "get-serialno").strip(" \r\n"))

                setattr(namespace, self.dest, wrapper)

        class EmulatorAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    return Device(Adb.exec("-e", "get-serialno").strip(" \r\n"))

                setattr(namespace, self.dest, wrapper)

        class ConnectAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    addr = str(values)
                    if addr.find(":") < 0:
                        addr = addr + ":5555"
                    devices = Adb.devices()
                    if addr not in [device.id for device in devices]:
                        Adb.exec("connect", addr, output_to_logger=True)
                    return Device(addr)

                setattr(namespace, self.dest, wrapper)

        class LastAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    if os.path.exists(cache_path):
                        with open(cache_path, "rt") as fd:
                            result = fd.read().strip()
                            if len(result) > 0:
                                return Device(result)
                    raise AdbError("no device used last time")

                setattr(namespace, self.dest, wrapper)

        group = parser.add_argument_group(title="adb arguments").add_mutually_exclusive_group()
        group.add_argument("-s", "--serial", metavar="SERIAL", dest="parse_device", action=SerialAction,
                           help="use device with given serial (adb -s option)", default=parse_device)
        group.add_argument("-d", "--device", dest="parse_device", nargs=0, const=True, action=DeviceAction,
                           help="use USB device (adb -d option)")
        group.add_argument("-e", "--emulator", dest="parse_device", nargs=0, const=True, action=EmulatorAction,
                           help="use TCP/IP device (adb -e option)")
        group.add_argument("-c", "--connect", metavar="IP[:PORT]", dest="parse_device", action=ConnectAction,
                           help="use device with TCP/IP")
        group.add_argument("-l", "--last", dest="parse_device", nargs=0, const=True, action=LastAction,
                           help="use last device")


class IOSCommand(Command, ABC):

    @property
    def _known_errors(self) -> Tuple[Type[BaseException]]:
        from linktools.ios import SibError
        return SibError,

    def _add_base_arguments(self, parser: ArgumentParser):
        super()._add_base_arguments(parser)

        from linktools.ios import Sib, SibError, Device
        cache_path = environ.resource.get_temp_path("cache", "device", "ios", create_parent=True)

        def parse_handler(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                device = fn(*args, **kwargs)
                if device is not None:
                    with open(cache_path, "wt+") as fd:
                        fd.write(device.id)
                return device

            return wrapper

        @parse_handler
        def parse_device():
            devices = Sib.devices()
            if len(devices) == 0:
                raise SibError("no devices/emulators found")

            if len(devices) == 1:
                return devices[0]

            table = Table(show_lines=True)
            table.add_column("Index", justify="right", style="cyan", no_wrap=True)
            table.add_column("UDID", style="magenta")
            table.add_column("Name", style="magenta")

            offset = 1
            for i in range(len(devices)):
                table.add_row(
                    str(i + offset),
                    ignore_error(lambda: devices[i].id),
                    ignore_error(lambda: devices[i].name),
                )

            console = get_console()
            console.print(table)

            prompt = f"More than one device/emulator. {os.linesep}" \
                     f"Enter device index"
            choices = [str(i) for i in range(offset, len(devices) + offset, 1)]
            index = IntPrompt.ask(prompt, choices=choices, default=offset, console=console)

            return devices[index - offset]

        class UdidAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    return Device(str(values))

                setattr(namespace, self.dest, wrapper)

        class LastAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    if os.path.exists(cache_path):
                        with open(cache_path, "rt") as fd:
                            result = fd.read().strip()
                            if len(result) > 0:
                                return Device(result)
                    raise SibError("no device used last time")

                setattr(namespace, self.dest, wrapper)

        class ConnectAction(Action):

            def __call__(self, parser, namespace, values, option_string=None):
                @parse_handler
                def wrapper():
                    address = str(values)
                    host, port = address.split(":", maxsplit=1)
                    Sib.exec("remote", "connect", "--host", host, "--port", port, output_to_logger=True)
                    for device in Sib.devices():
                        if address == device.address:
                            return device

                setattr(namespace, self.dest, wrapper)

        group = parser.add_argument_group(title="sib arguments")
        group = group.add_mutually_exclusive_group()
        group.add_argument("-u", "--udid", metavar="UDID", dest="parse_device", action=UdidAction,
                           help="specify unique device identifier", default=parse_device)
        group.add_argument("-c", "--connect", metavar="IP:PORT", dest="parse_device", action=ConnectAction,
                           help="use device with TCP/IP")
        group.add_argument("-l", "--last", dest="parse_device", nargs=0, const=True, action=LastAction,
                           help="use last device")
