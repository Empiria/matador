#!/usr/bin/env python
import platform


class Hello(object):

    def execute(self):
        print("Hello World")
        print(platform.python_version())
