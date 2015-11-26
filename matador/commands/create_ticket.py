#!/usr/bin/env python
from .command import Command
from matador.session import Session
import os


class CreateTicket(Command):

    def _add_arguments(self, parser):
        parser.prog = 'matador create-ticket'

        parser.add_argument(
            '-t', '--ticket',
            type=str,
            required=True,
            help='Ticket name')

    def _execute(self):
        Session.initialise_session()
        ticket_folder = os.path.join(
            Session.project_folder, 'deploy', 'tickets', self.args.ticket)
        os.makedirs(ticket_folder)
        deploy_file = os.path.join(ticket_folder, 'deploy.py')
        with open(deploy_file, 'w') as f:
            f.write('from matador.commands.deployment import *\n\n')
            f.close()
