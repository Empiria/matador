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
        args, sub_args = parser.parse_known_args()
        command = commands[args.command](parser)
    except:
        parser.print_help()
        sys.exit()

    command.execute()
