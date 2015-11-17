#!/usr/bin/env python
import sys
import logging


class Command(object):

    def __init__(self, parser):
        self._logger = logging.getLogger(__name__)
        self.add_arguments(parser)
        self.args = parser.parse_args()

    def add_arguments(self):
        pass

    def execute():
        raise NotImplementedError
