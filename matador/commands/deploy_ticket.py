#!/usr/bin/env python
from .command import Command
from matador import utils


class DeployTicket(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador deploy-ticket'
        parser.add_argument(
            '-e', '--environment',
            type=str,
            required=True,
            help='Agresso environment name')

        parser.add_argument(
            '-', '--package',
            type=bool,
            default=False,
            help='Agresso environment name')

    def _execute(self):
        project = utils.project()
        if not self.args.package:
            utils.update_repository(project)
