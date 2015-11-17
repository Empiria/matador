#!/usr/bin/env python
from matador.core.commands import commands


def execute_command(name):

    command = commands[name]()
    command.execute()
