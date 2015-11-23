#!/usr/bin/env python
import os
import subprocess
from matador.session import Session
from .deployment import DeploymentCommand, substitute_keywords
from matador.commands.run_sql_script import run_sql_script


class DeploySqlScript(DeploymentCommand):

    def _execute(self):
        scriptPath = self.args[0]

        if len(os.path.dirname(scriptPath)) == 0:
            targetScript = os.path.join(Session.ticket_folder, scriptPath)
        else:
            repo_folder = Session.matador_repository_folder
            scriptPath = os.path.join(repo_folder, self.args[0])
            targetScript = os.path.join(
                Session.ticket_folder, os.path.basename(scriptPath))
            commit = self.args[1]

            subprocess.run(
                ['git', '-C', repo_folder, 'checkout', commit],
                stderr=subprocess.STDOUT,
                stdout=open(os.devnull, 'w'),
                check=True)

            originalFile = open(scriptPath, 'r')
            originalText = originalFile.read()
            newText = substitute_keywords(
                originalText, repo_folder, commit)
            originalFile.close()

            newFile = open(targetScript, 'w')
            newFile.write(newText)
            newFile.close()

        run_sql_script(self._logger, targetScript)
