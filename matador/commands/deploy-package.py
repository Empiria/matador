#!/usr/bin/env python
from .command import Command


class ActionPackage(Command):
    action = 'None'

    def _add_arguments(self, parser):
        pass

    def _execute(self):
        pass


class DeployPackage(ActionPackage):
    action = 'deploy'


class RemovePackage(ActionPackage):
    action = 'remove'
