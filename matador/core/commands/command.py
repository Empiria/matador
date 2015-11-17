#!/usr/bin/env python
import sys


class Command(object):

    def __init__(self, parser):
        self.add_arguments(parser)
        self.args = parser.parse_args()

    def add_arguments(self):
        pass

    def execute():
        raise NotImplementedError
