#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : frida.py
@time    : 2021/12/18
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
import time

import frida

from .. import get_logger, utils

_logger = get_logger("frida.server")


class FridaServer(utils.get_derived_type(frida.core.Device), metaclass=abc.ABCMeta):  # proxy for frida.core.Device

    def __init__(self, device: frida.core.Device):
        super().__init__(device)

    @property
    def is_running(self) -> bool:
        """
        判断服务端运行状态
        :return: 是否正在运行
        """
        try:
            processes = self.enumerate_processes()
            return processes is not None
        except (frida.TransportError, frida.ServerNotRunningError):
            return False

    def start(self) -> bool:
        """
        根据frida版本和设备abi类型下载并运行server
        :return: 运行成功为True，否则为False
        """
        if self.is_running:
            _logger.info("Frida server is running ...")
            return True

        _logger.info("Start frida server ...")
        self._start()

        timeout = utils.Timeout(10)
        while timeout.check():
            if self.is_running:
                _logger.info("Frida server is running ...")
                return True
            time.sleep(min(timeout.remain, 0.5))

        raise frida.ServerNotRunningError("Frida server failed to run ...")

    def stop(self) -> bool:
        """
        强制结束frida server
        :return: 结束成功为True，否则为False
        """
        _logger.info("Kill frida server ...")
        try:
            self._stop()
            return True
        except frida.ServerNotRunningError:
            return True
        except:
            return False

    @abc.abstractmethod
    def _start(self):
        pass

    @abc.abstractmethod
    def _stop(self):
        pass

    def __enter__(self):
        try:
            self.start()
        except:
            self.stop()
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
