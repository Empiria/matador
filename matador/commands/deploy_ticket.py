#!/usr/bin/env python
from .command import Command
from matador import management
from matador import utils


class DeployTicket(Command):

    def _execute(self):
        working_folder = management.working_folder('uog01', 'dev')
        self._logger.info(working_folder)
        self._logger.info(utils.is_git_repository())
