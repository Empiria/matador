#!/usr/bin/env python
import sys
import logging
import argparse


class Command(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Taming the bull: Change management for Agresso systems")
        self._logger = logging.getLogger(__name__)
        self._add_arguments(parser)
        try:
            self.args, unknown = parser.parse_known_args()
        except:
            parser.print_help()
            sys.exit()
        self._execute()

    def _add_arguments(self, parser):
        pass

    def _execute(self):
        raise NotImplementedError
