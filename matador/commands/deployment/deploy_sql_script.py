#!/usr/bin/env python
import os
from pathlib import Path
import subprocess
from matador.session import Session
from .deployment import DeploymentCommand, substitute_keywords
from matador.commands.run_sql_script import run_sql_script


def _checkout_script(path, commit):
    repo_folder = Session.matador_repository_folder
    scriptPath = Path(repo_folder, path)
    targetScript = Path(
        Session.deployment_folder, scriptPath.name)

    subprocess.run(
        ['git', '-C', str(repo_folder), 'checkout', commit],
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

    return targetScript


class DeploySqlScript(DeploymentCommand):

    def _execute(self):
        path = self.args[0]

        if len(os.path.dirname(path)) == 0:
            targetScript = os.path.join(Session.deployment_folder, path)
        else:
            commit = self.args[1]
            targetScript = _checkout_script(path, commit)

        run_sql_script(self._logger, targetScript)


class DeployOraclePackage(DeploymentCommand):

    def _execute(self):
        packageName = self.args[0]
        commit = self.args[1]

        repo_folder = Session.matador_repository_folder
        package = os.path.join(
            repo_folder, 'src', 'db_objects', 'packages', packageName,
            packageName)
        packageSpec = package + '.pks'
        packageBody = package + '.pkb'

        packageSpecScript = _checkout_script(packageSpec, commit)
        packageBodyScript = _checkout_script(packageBody, commit)

        run_sql_script(self._logger, packageSpecScript)
        run_sql_script(self._logger, packageBodyScript)
