#!/usr/bin/env python
from .command import Command
from matador import utils


class DeployTicket(Command):

    def _execute(self):
        project_folder = utils.project_folder()
        self._logger.info(project_folder)

        working_folder = utils.working_folder('uog01', 'dev')
        self._logger.info(working_folder)

        project = utils.project()
        self._logger.info(project)

        self._logger.info(utils.is_git_repository())

