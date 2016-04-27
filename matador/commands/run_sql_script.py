#!/usr/bin/env python
from pathlib import Path
import os
import subprocess
from string import Template
from .command import Command
from matador.session import Session


def _command(**kwargs):
    oracle_connection = Template(
        '${user}/${password}@${server}:${port}/${db_name}')
    mssql_host = Template('${server}:${port}')

    commands = {
        ('oracle', 'nt'): [
            'sqlplus', '-S', '-L', oracle_connection.substitute(kwargs)],
        ('mssql', 'posix'): [
            'fisql', '-S', mssql_host.substitute(kwargs),
            '-D', kwargs['db_name'], '-U', kwargs['user'],
            '-P', kwargs['password']
        ],
        ('mssql', 'nt'): [
            'sqlcmd', '-S', mssql_host.substitute(kwargs),
            '-D', kwargs['db_name'], '-U', kwargs['user'],
            '-P', kwargs['password']
        ],
    }
    commands[('oracle', 'posix')] = commands[('oracle', 'nt')]

    return commands[(kwargs['dbms'], os.name)]


def _sql_script(**kwargs):
    file = Path(kwargs['directory'], kwargs['file'])

    with file.open('r') as f:
        script = f.read()
        f.close()

    if kwargs['dbms'] == 'oracle':
        script += '\nshow error'

    return script.encode('utf-8')


def run_sql_script(logger, **kwargs):
    message = Template(
        'Matador: Executing ${file} against ${db_name} on ${server} \n')
    logger.info(message.substitute(kwargs))

    os.chdir(kwargs['directory'])

    process = subprocess.Popen(
        _command(**kwargs),
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process.stdin.write(_sql_script(**kwargs))
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
        kwargs = {
            **Session.environment['database'],
            **Session.credentials,
            **self.args}
        run_sql_script(self._logger, **kwargs)
