#!/usr/bin/env python3
"""
Script to execute an sql script against an oracle database using the sqlplus
client.

It can be used standalone or from within a sublime text build configuration.

Place this script in a directory included in the PATH environment variable.

For Sublime Text, create a .sublime-build file in the 'Packages/User' directory
with the following content:

    {
      "cmd":[
          "oracle_sql.py",
          "-d", "$file_path",
          "-f", "$file_name",
          "-u", "<User ID>"",
          "-p", "<Password>",
          "-s", "<SID>"],
      "selector": "source.plsql.oracle"
    }

The "selector" entry assumes that package 'Oracle PL SQL' is installed.
"""
import os
import sys
import argparse
import subprocess
from string import Template

parser = argparse.ArgumentParser(
    description="Pass an sql script to Oracle")

parser.add_argument(
    '-d',
    '--directory',
    type=str,
    dest='directory',
    help='Path to directory containing sql script')

parser.add_argument(
    '-f',
    '--file',
    type=str,
    dest='file_name',
    help='Full file name of sql script')

parser.add_argument(
    '-u',
    '--user',
    type=str,
    dest='user',
    help='Oracle user name')

parser.add_argument(
    '-p',
    '--password',
    type=str,
    dest='password',
    help='Oracle password')

parser.add_argument(
    '-s',
    '--sid',
    type=str,
    dest='sid',
    help='Oracle SID')

try:
    args = parser.parse_args()
    file_path = os.path.join(args.directory, args.file_name)
except:
    parser.print_help()
    sys.exit(0)

connection = args.user + '/' + args.password + '@' + args.sid

file = open(file_path, 'r')
script = file.read()
script += '\nshow error'

os.chdir(args.directory)

message = Template('Executing ${file_name} against ${sid} \n')
substitutions = {
    'file_name': args.file_name,
    'sid': args.sid
    }
print(message.substitute(substitutions))
sys.stdout.flush()

process = subprocess.Popen(
    ['sqlplus', '-S', '-L', connection],
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE)
process.stdin.write(script.encode('utf-8'))
process.stdin.close()
process.wait()
