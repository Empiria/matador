#!/usr/bin/env python
import os
import subprocess
from string import Template
from .command import Command
from matador.session import Session


def _connection_string(dbms, connection, user, password):
    if dbms.lower() == 'oracle':
        return user + '/' + password + '@' + connection


def _sql_script(file_path):
    file = open(file_path, 'r')
    script = file.read()
    return script


def runScript(logger, file_path, dbms, connection):
        script = _sql_script(file_path)

        message = Template(
            'Matador: Executing ${file} against ${connection} \n')
        substitutions = {
            'file': os.path.basename(file_path),
            'connection': Session.environment['connection']
        }
        logger.info(message.substitute(substitutions))

        os.chdir(os.path.dirname(file_path))

        if dbms.lower() == 'oracle':
            script += '\nshow error'
            process = subprocess.Popen(
                ['sqlplus', '-S', '-L', connection],
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE)
            process.stdin.write(script.encode('utf-8'))
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
        file_path = os.path.join(self.args.directory, self.args.file)

        connection_string = _connection_string(
            Session.environment['dbms'],
            Session.environment['connection'],
            Session.credentials['user'],
            Session.credentials['password'])
        runScript(
            self._logger,
            file_path,
            Session.environment['dbms'],
            connection_string)
