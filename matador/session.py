#!/usr/bin/env python
import os
import subprocess
import yaml
import sys


def get_environments(project_folder):
    file_path = os.path.join(
        project_folder, 'config', 'environments.yml')
    try:
        file = open(file_path, 'r')
    except FileNotFoundError:
        print('Cannot find environments.yml file')
        sys.exit()
    return yaml.load(file)


def get_credentials(project_folder):
    file_path = os.path.join(
        project_folder, 'config', 'credentials.yml')
    try:
        file = open(file_path, 'r')
    except FileNotFoundError:
        print('Cannot find credentials.yml file')
        sys.exit()
    return yaml.load(file)


def initialise_repository(proj_folder, repo_folder):
    subprocess.run([
        'git', '-C', repo_folder, 'init'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w'))

    subprocess.run([
        'git', '-C', repo_folder, 'config', 'core.sparsecheckout', 'true'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w'))

    subprocess.run([
        'git', '-C', repo_folder, 'remote', 'add', 'origin', proj_folder],
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
        f.write('src/ filter=substitution\n')
        f.close()

    sparse_checkout_file = os.path.join(
        git_path, 'info', 'sparse-checkout')
    with open(sparse_checkout_file, 'a') as f:
        f.write('/src\n')
        f.write('/deploy\n')
        f.close()


class Session(object):

    project_folder = subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        stderr=subprocess.STDOUT).decode('utf-8').strip('\n')

    project = os.path.basename(project_folder)

    matador_project_folder = os.path.expanduser('~/.matador/%s' % project)

    matador_repository_folder = os.path.join(
        matador_project_folder, 'repository')

    is_git_repository = subprocess.run(
        ['git', 'status'],
        stderr=subprocess.STDOUT,
        stdout=open(os.devnull, 'w')) == 0

    environments = get_environments(project_folder)

    os.makedirs(matador_project_folder, exist_ok=True)
    os.makedirs(matador_repository_folder, exist_ok=True)

    initialise_repository(project_folder, matador_repository_folder)

    environment = None

    @classmethod
    def set_environment(self, environment):
        if self.environment is not None:
            return
        else:
            self.environment = self.environments[environment]
            credentials = get_credentials(self.project_folder)
            self.credentials = credentials[environment]

            self.matador_environment_folder = os.path.join(
                self.matador_project_folder, environment)
            self.matador_tickets_folder = os.path.join(

                self.matador_environment_folder, 'tickets')

            os.makedirs(self.matador_environment_folder, exist_ok=True)
            os.makedirs(self.matador_tickets_folder, exist_ok=True)

    @classmethod
    def update_repository(self):
        repo_folder = self.matador_repository_folder

        if not self.is_git_repository:
            proj_folder = self.project_folder
            initialise_repository(proj_folder, repo_folder)

        subprocess.run(
            ['git', '-C', repo_folder, 'fetch', '-a'],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))

        subprocess.run(
            ['git', '-C', repo_folder, 'checkout', '-b', 'empty'],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))

        empty_file = os.path.join(repo_folder, '.empty')
        with open(empty_file, 'a') as f:
            f.write('Minimal file for empty working directory')

        subprocess.run(
            ['git', '-C', repo_folder, 'add', '-A'],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))

        subprocess.run(
            ['git', '-C', repo_folder, 'commit', '-m', 'Empty'],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))
