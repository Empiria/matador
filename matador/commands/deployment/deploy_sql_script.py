#!/usr/bin/env python
import os
from matador.session import Session
from .deployment_command import DeploymentCommand
from matador.commands.run_sql_script import run_sql_script


class DeploySqlScript(DeploymentCommand):

    def _execute(self):
        os.chdir(Session.project_folder)
        run_sql_script(
            self._logger,
            self.args[0])
