#!/usr/bin/env python
import os
import subprocess


def working_folder(project, environment):
    working_path = os.path.expanduser(
        '~/.matador/%s/%s' % (project, environment))
    os.makedirs(working_path, exist_ok=True)
    return working_path


def is_git_repository(path='.'):
    return subprocess.call(
        ['git', '-C', path, 'status'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w')) == 0

