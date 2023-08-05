#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Datetime  : 2023/1/18 11:30
# Author    : HuJi <jihu.hj@alibaba-inc.com>

from argparse import ArgumentParser
from typing import Optional

from prompt_toolkit import Application, print_formatted_text
from prompt_toolkit.layout import FormattedTextControl, Window, WindowAlign
from prompt_toolkit.shortcuts import print_container
from prompt_toolkit.widgets import Frame

from linktools import cli


class Command(cli.Command):
    """
    Start repl command console
    """

    def _add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def _run(self, args: [str]) -> Optional[int]:
        args = self.argument_parser.parse_args(args)

        for i in range(1000):
            print_formatted_text()
            print_container(
                Window(
                    FormattedTextControl(text=f"{i}"),
                    # align=WindowAlign.RIGHT,
                    # style="class:rprompt",
                )
            )
            print(i)



command = Command()
if __name__ == "__main__":
    command.main()
