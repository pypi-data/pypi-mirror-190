#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright 2009, The Android Open Source Project
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Script to highlight adb logcat output for console
# Originally written by Jeff Sharkey, http://jsharkey.org/
# Piping detection and popen() added by other Android team members
# Package filtering and output improvements by Jake Wharton, http://jakewharton.com

import re
import sys
from argparse import ArgumentParser
from subprocess import PIPE
from typing import Optional

from linktools import cli

__version__ = '2.1.0'

LOG_LEVELS = 'VDIWEF'
LOG_LEVELS_MAP = dict([(LOG_LEVELS[i], i) for i in range(len(LOG_LEVELS))])

widths = [
    (126, 1), (159, 0), (687, 1), (710, 0), (711, 1),
    (727, 0), (733, 1), (879, 0), (1154, 1), (1161, 0),
    (4347, 1), (4447, 2), (7467, 1), (7521, 0), (8369, 1),
    (8426, 0), (9000, 1), (9002, 2), (11021, 1), (12350, 2),
    (12351, 1), (12438, 2), (12442, 0), (19893, 2), (19967, 1),
    (55203, 2), (63743, 1), (64106, 2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376, 2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]


def get_char_width(char):
    global widths
    o = ord(char)
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= num:
            return wid
    return 1


class Command(cli.AndroidCommand):
    """
    Filter logcat by package name
    """

    def _add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('package', nargs='*', help='application package name(s)')
        parser.add_argument('-w', '--tag-width', metavar='N', dest='tag_width', type=int, default=23,
                            help='width of log tag')
        parser.add_argument('-l', '--min-level', dest='min_level', type=str, choices=LOG_LEVELS + LOG_LEVELS.lower(),
                            default='V', help='minimum level to be displayed')
        parser.add_argument('--color-gc', dest='color_gc', action='store_true', help='color garbage collection')
        parser.add_argument('--always-display-tags', dest='always_tags', action='store_true',
                            help='always display the tag name')
        parser.add_argument('--top', '--current', dest='current_app', action='store_true',
                            help='filter logcat by current running app')
        parser.add_argument('-c', '--clear', dest='clear_logcat', action='store_true',
                            help='clear the entire log before running')
        parser.add_argument('-t', '--tag', dest='tag', action='append', help='filter output by specified tag(s)')
        parser.add_argument('-i', '--ignore-tag', dest='ignored_tag', action='append',
                            help='filter output by ignoring specified tag(s)')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__,
                            help='print the version number and exit')
        parser.add_argument('-a', '--all', dest='all', action='store_true', default=False,
                            help='print all log messages')

    def _run(self, args: [str]) -> Optional[int]:
        args = self.argument_parser.parse_args(args)
        device = args.parse_device()
        package = args.package
        min_level = LOG_LEVELS_MAP[args.min_level.upper()]

        if args.current_app:
            package.append(device.get_current_package())

        if len(package) == 0:
            args.all = True

        # Store the names of packages for which to match all processes.
        catchall_package = list(filter(lambda package: package.find(":") == -1, package))
        # Store the name of processes to match exactly.
        named_processes = list(filter(lambda package: package.find(":") != -1, package))
        # Convert default process names from <package>: (cli notation) to <package> (android notation) in the exact names match group.
        named_processes = list(map(lambda package: package if package.find(":") != len(package) - 1 else package[:-1],
                                   named_processes))

        header_size = args.tag_width + 1 + 3 + 1  # space, level, space

        width = -1
        try:
            # Get the current terminal width
            import fcntl, termios, struct

            h, width = struct.unpack('hh', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('hh', 0, 0)))
        except:
            pass

        BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

        RESET = '\033[0m'

        def termcolor(fg=None, bg=None):
            codes = []
            if fg is not None: codes.append('3%d' % fg)
            if bg is not None: codes.append('10%d' % bg)
            return '\033[%sm' % ';'.join(codes) if codes else ''

        def colorize(message, fg=None, bg=None):
            return termcolor(fg, bg) + message + RESET

        def truncated_string(message, offset, width):
            next = offset
            length = len(message)
            while next < length:
                width = width - get_char_width(message[next])
                if width < 0:
                    break
                next = next + 1
            return next

        def indent_wrap(message):
            if width == -1:
                return message
            message = message.replace('\t', '    ')
            wrap_area = width - header_size - 1
            messagebuf = ''
            current = 0
            next = truncated_string(message, current, wrap_area)
            while current < next:
                messagebuf += message[current:next]
                if next < len(message):
                    messagebuf += '\n'
                    messagebuf += ' ' * header_size
                current = next
                next = truncated_string(message, current, wrap_area)
            return messagebuf

        LAST_USED = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
        KNOWN_TAGS = {
            'dalvikvm': WHITE,
            'Process': WHITE,
            'ActivityManager': WHITE,
            'ActivityThread': WHITE,
            'AndroidRuntime': CYAN,
            'jdwp': WHITE,
            'StrictMode': WHITE,
            'DEBUG': YELLOW,
        }

        def allocate_color(tag):
            # this will allocate a unique format for the given tag
            # since we dont have very many colors, we always keep track of the LRU
            if tag not in KNOWN_TAGS:
                KNOWN_TAGS[tag] = LAST_USED[0]
            color = KNOWN_TAGS[tag]
            if color in LAST_USED:
                LAST_USED.remove(color)
                LAST_USED.append(color)
            return color

        RULES = {
            # StrictMode policy violation; ~duration=319 ms: android.os.StrictMode$StrictModeDiskWriteViolation: policy=31 violation=1
            re.compile(r'^(StrictMode policy violation)(; ~duration=)(\d+ ms)')
            : r'%s\1%s\2%s\3%s' % (termcolor(RED), RESET, termcolor(YELLOW), RESET),
        }

        # Only enable GC coloring if the user opted-in
        if args.color_gc:
            # GC_CONCURRENT freed 3617K, 29% free 20525K/28648K, paused 4ms+5ms, total 85ms
            key = re.compile(
                r'^(GC_(?:CONCURRENT|FOR_M?ALLOC|EXTERNAL_ALLOC|EXPLICIT) )(freed <?\d+.)(, \d+\% free \d+./\d+., )(paused \d+ms(?:\+\d+ms)?)')
            val = r'\1%s\2%s\3%s\4%s' % (termcolor(GREEN), RESET, termcolor(YELLOW), RESET)

            RULES[key] = val

        TAGTYPES = {
            'V': colorize(' V ', fg=WHITE, bg=BLACK),
            'D': colorize(' D ', fg=BLACK, bg=BLUE),
            'I': colorize(' I ', fg=BLACK, bg=GREEN),
            'W': colorize(' W ', fg=BLACK, bg=YELLOW),
            'E': colorize(' E ', fg=BLACK, bg=RED),
            'F': colorize(' F ', fg=BLACK, bg=RED),
        }

        PID_LINE = re.compile(r'^\w+\s+(\w+)\s+\w+\s+\w+\s+\w+\s+\w+\s+\w+\s+\w\s([\w|\.|\/]+)$')
        PID_START = re.compile(r'^.*: Start proc ([a-zA-Z0-9._:]+) for ([a-z]+ [^:]+): pid=(\d+) uid=(\d+) gids=(.*)$')
        PID_START_5_1 = re.compile(r'^.*: Start proc (\d+):([a-zA-Z0-9._:]+)/[a-z0-9]+ for (.*)$')
        PID_START_DALVIK = re.compile(
            r'^E/dalvikvm\(\s*(\d+)\): >>>>> ([a-zA-Z0-9._:]+) \[ userId:0 \| appId:(\d+) \]$')
        PID_KILL = re.compile(r'^Killing (\d+):([a-zA-Z0-9._:]+)/[^:]+: (.*)$')
        PID_LEAVE = re.compile(r'^No longer want ([a-zA-Z0-9._:]+) \(pid (\d+)\): .*$')
        PID_DEATH = re.compile(r'^Process ([a-zA-Z0-9._:]+) \(pid (\d+)\) has died.?$')
        LOG_LINE = re.compile(r'^([A-Z])/(.+?)\( *(\d+)\): (.*?)$')
        BUG_LINE = re.compile(r'.*nativeGetEnabledTags.*')
        BACKTRACE_LINE = re.compile(r'^#(.*?)pc\s(.*?)$')

        adb_command = ['logcat', '-v', 'brief']

        # Clear log before starting logcat
        if args.clear_logcat:
            adb_clear_command = list(adb_command)
            adb_clear_command.append('-c')
            adb_clear = device.popen(*adb_clear_command)

            while adb_clear.poll() is None:
                pass

        # This is a ducktype of the device.popen object
        class FakeStdinProcess():
            def __init__(self):
                self.stdout = sys.stdin

            def poll(self):
                return None

        if sys.stdin.isatty():
            adb = device.popen(*adb_command, stdin=PIPE, stdout=PIPE)
        else:
            adb = FakeStdinProcess()
        pids = set()
        last_tag = None
        app_pid = None

        def match_packages(token):
            if len(package) == 0:
                return True
            if token in named_processes:
                return True
            index = token.find(':')
            return (token in catchall_package) if index == -1 else (token[:index] in catchall_package)

        def parse_death(tag, message):
            if tag != 'ActivityManager':
                return None, None
            kill = PID_KILL.match(message)
            if kill:
                pid = kill.group(1)
                package_line = kill.group(2)
                if match_packages(package_line) and pid in pids:
                    return pid, package_line
            leave = PID_LEAVE.match(message)
            if leave:
                pid = leave.group(2)
                package_line = leave.group(1)
                if match_packages(package_line) and pid in pids:
                    return pid, package_line
            death = PID_DEATH.match(message)
            if death:
                pid = death.group(2)
                package_line = death.group(1)
                if match_packages(package_line) and pid in pids:
                    return pid, package_line
            return None, None

        def parse_start_proc(line):
            start = PID_START_5_1.match(line)
            if start is not None:
                line_pid, line_package, target = start.groups()
                return line_package, target, line_pid, '', ''
            start = PID_START.match(line)
            if start is not None:
                line_package, target, line_pid, line_uid, line_gids = start.groups()
                return line_package, target, line_pid, line_uid, line_gids
            start = PID_START_DALVIK.match(line)
            if start is not None:
                line_pid, line_package, line_uid = start.groups()
                return line_package, '', line_pid, line_uid, ''
            return None

        def tag_in_tags_regex(tag, tags):
            return any(re.match(r'^' + t + r'$', tag) for t in map(str.strip, tags))

        for line in device.shell("ps").splitlines():
            pid_match = PID_LINE.match(line.strip())
            if pid_match is not None:
                pid = pid_match.group(1)
                proc = pid_match.group(2)
                if proc in catchall_package:
                    seen_pids = True
                    pids.add(pid)

        for line in device.shell("ps", "-A").splitlines():
            pid_match = PID_LINE.match(line.strip())
            if pid_match is not None:
                pid = pid_match.group(1)
                proc = pid_match.group(2)
                if proc in catchall_package:
                    seen_pids = True
                    pids.add(pid)

        while adb.poll() is None:
            try:
                line = adb.stdout.readline().decode('utf-8', errors="ignore").strip()
            except KeyboardInterrupt:
                break

            bug_line = BUG_LINE.match(line)
            if bug_line is not None:
                continue

            log_line = LOG_LINE.match(line)
            if log_line is None:
                continue

            level, tag, owner, message = log_line.groups()
            tag = tag.strip()
            start = parse_start_proc(line)
            if start:
                line_package, target, line_pid, line_uid, line_gids = start

                if match_packages(line_package):
                    pids.add(line_pid)

                    app_pid = line_pid

                    linebuf = '\n'
                    linebuf += colorize(' ' * (header_size - 1), bg=WHITE)
                    linebuf += indent_wrap(' Process %s created for %s\n' % (line_package, target))
                    linebuf += colorize(' ' * (header_size - 1), bg=WHITE)
                    linebuf += ' PID: %s    UID: %s    GIDs: %s' % (line_pid, line_uid, line_gids)
                    linebuf += '\n'
                    print(linebuf)
                    last_tag = None  # Ensure next log gets a tag printed

            dead_pid, dead_pname = parse_death(tag, message)
            if dead_pid:
                pids.remove(dead_pid)
                linebuf = '\n'
                linebuf += colorize(' ' * (header_size - 1), bg=RED)
                linebuf += ' Process %s (PID: %s) ended' % (dead_pname, dead_pid)
                linebuf += '\n'
                print(linebuf)
                last_tag = None  # Ensure next log gets a tag printed

            # Make sure the backtrace is printed after a native crash
            if tag == 'DEBUG':
                bt_line = BACKTRACE_LINE.match(message.lstrip())
                if bt_line is not None:
                    message = message.lstrip()
                    owner = app_pid

            if not args.all and owner not in pids:
                continue
            if level in LOG_LEVELS_MAP and LOG_LEVELS_MAP[level] < min_level:
                continue
            if args.ignored_tag and tag_in_tags_regex(tag, args.ignored_tag):
                continue
            if args.tag and not tag_in_tags_regex(tag, args.tag):
                continue

            linebuf = ''

            if args.tag_width > 0:
                # right-align tag title and allocate color if needed
                if tag != last_tag or args.always_tags:
                    last_tag = tag
                    color = allocate_color(tag)
                    tag = tag[-args.tag_width:].rjust(args.tag_width)
                    linebuf += colorize(tag, fg=color)
                else:
                    linebuf += ' ' * args.tag_width
                linebuf += ' '

            # write out level colored edge
            if level in TAGTYPES:
                linebuf += TAGTYPES[level]
            else:
                linebuf += ' ' + level + ' '
            linebuf += ' '

            # format tag message using rules
            for matcher in RULES:
                replace = RULES[matcher]
                message = matcher.sub(replace, message)

            linebuf += indent_wrap(message)
            print(linebuf)


command = Command()
if __name__ == "__main__":
    command.main()
