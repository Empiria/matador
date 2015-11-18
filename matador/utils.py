#!/usr/bin/env python
import os
import subprocess


def is_git_repository(path='.'):
    return subprocess.call(
        ['git', '-C', path, 'status'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w')) == 0
