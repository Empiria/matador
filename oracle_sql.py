#!/usr/bin/env python3
"""
Script to execute an sql script against an oracle database using the sqlplus
client.

It can be used standalone or from within a sublime text build configuration.
"""
import os
import sys
import argparse
import subprocess

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

file = open(file_path, 'r')
connection = args.user + '/' + args.password + '@' + args.sid

os.chdir(args.directory)

subprocess.run(
    ['sqlplus', '-S', '-L', connection], stdin=file)
print('Executed %s against %s' % (args.file_name, args.sid))
