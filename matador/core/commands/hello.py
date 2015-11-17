#!/usr/bin/env python
from .command import Command
import platform


class Hello(Command):

    def add_arguments(self, parser):
        parser.add_argument(
            '-m', '--message',
            type=str,
            dest='message',
            required=True,
            help='Message')

    def execute(self):
        print("Hello")
        print(self.args.message)
        print(platform.python_version())
        print
