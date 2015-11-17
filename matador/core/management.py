#!/usr/bin/env python
import sys
import logging
import argparse
from matador.core.commands import commands


def setup_logging(logging_destination='console', verbosity='DEBUG'):
    logHandlers = {
        'console': logging.StreamHandler(),
        'none': logging.NullHandler(),
        'file': logging.FileHandler('./axelrod.log')
    }
    logHandler = logHandlers[logging_destination]

    logFormatters = {
        'console': '%(message)s',
        'none': '',
        'file': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    logFormatter = logging.Formatter(logFormatters[logging_destination])

    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('matador')
    level = logging.getLevelName(verbosity.upper())
    logger.setLevel(level)
    logger.addHandler(logHandler)


def execute_command():
    setup_logging()
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
