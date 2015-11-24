#!/usr/bin/env python
from .command import Command


class ActionPackage(Command):
    action = 'None'

    def _add_arguments(self, parser):
        parser.prog = 'matador deploy-package'
        parser.add_argument(
            '-e', '--environment',
            type=str,
            required=True,
            help='Agresso environment name')

        parser.add_argument(
            '-p', '--package',
            type=str,
            required=True,
            help='Ticket name')

        parser.add_argument(
            '-c', '--commit',
            type=str,
            default='none',
            help='Branch name')

    def _execute(self):
        pass


class DeployPackage(ActionPackage):
    action = 'deploy'


class RemovePackage(ActionPackage):
    action = 'remove'
