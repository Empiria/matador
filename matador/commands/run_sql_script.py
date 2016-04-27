#!/usr/bin/env python
from pathlib import Path
import os
import subprocess
from string import Template
from .command import Command
from matador.session import Session


def _command(dbms, connection, user, password):
    commands = {
        ('oracle', 'nt'): [
            'sqlplus', '-S', '-L', user + '/' + password + '@' + connection],
        ('mssql', 'posix'): ['fisql'],
        ('mssql', 'nt'): ['sqlcmd']
    }
    commands[('oracle', 'posix')] = commands[('oracle', 'nt')]

    return commands[(dbms, os.name)]


def _sql_script(dbms, file_path):
    with file_path.open('r') as f:
        script = f.read()
        f.close()

    if dbms == 'oracle':
        script += '\nshow error'

    return script.encode('utf-8')


def run_sql_script(logger, dbms, connection, user, password, file_path):
    file = Path(file_path)
    message = Template(
        'Matador: Executing ${file} against ${connection} \n')
    substitutions = {
        'file': file.name,
        'connection': Session.environment['connection']
    }
    logger.info(message.substitute(substitutions))

    os.chdir(str(file.parent))

    process = subprocess.Popen(
        _command(dbms, connection, user, password),
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process.stdin.write(_sql_script(dbms, file))
    process.stdin.close()
    process.wait()


class RunSqlScript(Command):

    def _add_arguments(self, parser):

        parser.add_argument(
            '-d', '--directory',
            type=str,
            required=True,
            help='Directory containing script')

        parser.add_argument(
            '-f', '--file',
            type=str,
            required=True,
            help='Script file name')

        parser.add_argument(
            '-e', '--environment',
            type=str,
            required=True,
            help='Agresso environment')

    def _execute(self):
        Session.set_environment(self.args.environment)

        file_path = os.path.join(self.args.directory, self.args.file)

        run_sql_script(
            self._logger,
            Session.environment['dbms'].lower(),
            Session.environment['connection'],
            Session.credentials['user'],
            Session.credentials['password'],
            file_path)
