#!/usr/bin/env python
import os
import subprocess
import yaml


def matador_project_folder(project):
    project_path = os.path.expanduser(
        '~/.matador/%s' % project)
    os.makedirs(project_path, exist_ok=True)
    return project_path


def matador_repository_folder(project):
    repository_path = os.path.join(
        matador_project_folder(project), 'repository')
    os.makedirs(repository_path, exist_ok=True)
    return repository_path


def matador_environment_folder(project, environment):
    working_path = os.path.join(
        matador_project_folder(project), environment)
    os.makedirs(working_path, exist_ok=True)
    return working_path


def matador_ticket_folder(project, environment):
    ticket_path = os.path.join(
        matador_environment_folder(project, environment), 'tickets')
    os.makedirs(ticket_path, exist_ok=True)
    return ticket_path


def is_git_repository(path='.'):
    return subprocess.run(
        ['git', '-C', path, 'status'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w')) == 0


def project_folder(path='.'):
    git_output = subprocess.check_output(
        ['git', '-C', path, 'rev-parse', '--show-toplevel'],
        stderr=subprocess.STDOUT)
    return git_output.decode('utf-8').strip('\n')


def project():
    return os.path.basename(project_folder())


def environments():
    file_path = os.path.join(
        project_folder(), 'config', 'environments.yml')
    file = open(file_path, 'r')
    return yaml.load(file)


def update_repository(project, branch='master'):
    repo_folder = matador_repository_folder(project)
    if not is_git_repository(repo_folder):
        subprocess.run(
            ['git', 'clone', '-n', '-b', branch, project_folder(), repo_folder],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))

        git_path = (os.path.join(repo_folder, '.git'))
        config_file = os.path.join(git_path, 'config')
        with open(config_file, 'a') as f:
            f.write('[filter "substitution"]\n')
            f.write('        smudge = matador substitute-keywords\n')
            f.write('        clean = matador clean-keywords\n')
            f.close()

        attributes_file = os.path.join(git_path, 'info', 'attributes')
        with open(attributes_file, 'a') as f:
            f.write('*.sql filter=substitution\n')
            f.write('*.pkb filter=substitution\n')
            f.write('*.pks filter=substitution\n')
            f.close()

    subprocess.run(
        ['git', '-C', repo_folder, 'fetch', 'origin', branch],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w'))
