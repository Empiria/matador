#!/usr/bin/env python
from pathlib import Path
import os
import subprocess
from string import Template
from .command import Command
from matador.session import Session


def _command(**db_args):
    oracle_connection = Template(
        '${user}/${password}@${server}:${port}/${db_name}')
    mssql_host = Template('${server}:${port}')

    commands = {
        ('oracle', 'nt'): [
            'sqlplus', '-S', '-L', oracle_connection.substitute(db_args)],
        ('mssql', 'posix'): [
            'fisql', '-S', mssql_host.substitute(db_args),
            '-D', db_args['db_name'], '-U', db_args['user'],
            '-P', db_args['password']
        ],
        ('mssql', 'nt'): [
            'sqlcmd', '-S', mssql_host.substitute(db_args),
            '-D', db_args['db_name'], '-U', db_args['user'],
            '-P', db_args['password']
        ],
    }
    commands[('oracle', 'posix')] = commands[('oracle', 'nt')]

    return commands[(db_args['dbms'], os.name)]


def _sql_script(dbms, file_path):
    with file_path.open('r') as f:
        script = f.read()
        f.close()

    if dbms == 'oracle':
        script += '\nshow error'

    return script.encode('utf-8')


def run_sql_script(logger, file_path, **db_args):
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
        _command(**db_args),
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    process.stdin.write(_sql_script(db_args['dbms'], file))
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
        db_args = {**Session.environment['database'], **Session.credentials}
        run_sql_script(self._logger, file_path, **db_args)
