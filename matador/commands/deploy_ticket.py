#!/usr/bin/env python
from .command import Command
from matador import management


class DeployTicket(Command):

    def _execute(self):
        self._logger.info(management.working_folder('uog01', 'dev'))

