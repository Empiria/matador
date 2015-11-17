#!/usr/bin/env python
import sys
import argparse
from matador.core.commands import commands


def execute_command():
    parser = argparse.ArgumentParser(
        description="Change management for Agresso")

    parser.add_argument(
        'command',
        type=str,
        help='Command')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    command = commands[args.command]()
    command.execute()
