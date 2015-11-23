#!/usr/bin/env python
import os
import shutil
import subprocess
from matador.session import Session
from .deployment_command import DeploymentCommand
from matador.commands.run_sql_script import run_sql_script


class DeploySqlScript(DeploymentCommand):

    def _execute(self):
        scriptPath = self.args[0]

        if len(os.dirname(scriptPath)) == 0:
            script = os.path.join(Session.ticket_folder, scriptPath)
        else:
            repo_folder = Session.matador_repository_folder
            scriptPath = os.path.join(repo_folder, self.args[0])
            commit = self.args[1]

            checkout = subprocess.check_call([
                'git', '-C', repo_folder, 'checkout', commit],
                stderr=subprocess.STDOUT,
                stdout=open(os.devnull, 'w'))

            if checkout == 0:
                script = shutil.copy(scriptPath, Session.ticket_folder)
            else:
                self._logger.info('Could not checkout %s' % commit)
                return

        run_sql_script(self._logger, script)
