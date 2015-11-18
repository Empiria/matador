#!/usr/bin/env python
from .command import Command
from matador.core import management


class DeployTicket(Command):

    def _execute(self):
        self._logger.info(management.working_folder())

