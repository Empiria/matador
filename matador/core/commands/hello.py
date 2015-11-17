#!/usr/bin/env python
from .command import Command
import platform


class Hello(Command):

    def execute(self):
        print("Hello World")
        print(platform.python_version())
