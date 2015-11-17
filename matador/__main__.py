#!/usr/bin/env python
import sys
import argparse
from matador.core import management

if __name__ == "__main__":

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

    management.execute_command(args.command)
