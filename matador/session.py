#!/usr/bin/env python
import os
import subprocess
import yaml
from dulwich import porcelain
from configparser import ConfigParser


def get_environments(project_folder):
        file_path = os.path.join(
            project_folder, 'config', 'environments.yml')
        file = open(file_path, 'r')
        return yaml.load(file)


def get_credentials(project_folder):
    file_path = os.path.join(
        project_folder, 'config', 'credentials.yml')
    file = open(file_path, 'r')
    return yaml.load(file)


def initialise_repository(proj_folder, repo_folder):
    config_file = (os.path.join(repo_folder, '.git', 'config'))
    config = ConfigParser()

    porcelain.init(repo_folder)
    config.read(config_file)

    config['core']['sparsecheckout'] = 'true'
    config['remote "origin"'] = {
        'url': proj_folder,
        'fetch': '+refs/heads/*:refs/remotes/origin/*'
    }

    with open(config_file, 'w') as f:
        f.write(config)
        f.close()

    sparse_checkout_file = os.path.join(
        repo_folder, '.git', 'info', 'sparse-checkout')
    with open(sparse_checkout_file, 'a') as f:
        f.write('/src\n')
        f.write('/deploy\n')
        f.close()


class Session(object):

    project_folder = None
    environment = None

    @classmethod
    def initialise_session(self):
        if self.project_folder is not None:
            return
        else:
            self.project_folder = subprocess.check_output(
                ['git', 'rev-parse', '--show-toplevel'],
                stderr=subprocess.STDOUT).decode('utf-8').strip('\n')

            self.project = os.path.basename(self.project_folder)

            self.matador_project_folder = os.path.expanduser(
                '~/.matador/%s' % self.project)

            self.matador_repository_folder = os.path.join(
                self.matador_project_folder, 'repository')

            self.environments = get_environments(self.project_folder)

    @classmethod
    def _initialise_matador_repository(self):
        os.makedirs(self.matador_project_folder, exist_ok=True)
        os.makedirs(self.matador_repository_folder, exist_ok=True)

        try:
            subprocess.run(
                ['git', '-C', self.matador_repository_folder, 'status'],
                stderr=subprocess.STDOUT,
                stdout=open(os.devnull, 'w'),
                check=True)
        except subprocess.CalledProcessError:
            initialise_repository(
                self.project_folder, self.matador_repository_folder)

    @classmethod
    def set_environment(self, environment):

        if self.environment is not None:
            return
        else:
            self._initialise_matador_repository()
            self.environment = self.environments[environment]
            credentials = get_credentials(self.project_folder)
            self.credentials = credentials[environment]

            self.matador_environment_folder = os.path.join(
                self.matador_project_folder, environment)
            self.matador_tickets_folder = os.path.join(
                self.matador_environment_folder, 'tickets')
            self.matador_packages_folder = os.path.join(
                self.matador_environment_folder, 'packages')

            os.makedirs(self.matador_environment_folder, exist_ok=True)
            os.makedirs(self.matador_tickets_folder, exist_ok=True)
            os.makedirs(self.matador_packages_folder, exist_ok=True)

    @classmethod
    def update_repository(self):
        repo_folder = self.matador_repository_folder

        try:
            subprocess.run(
                ['git', '-C', repo_folder, 'status'],
                stderr=subprocess.STDOUT,
                stdout=open(os.devnull, 'w'),
                check=True)
        except subprocess.CalledProcessError:
            proj_folder = self.project_folder
            initialise_repository(proj_folder, repo_folder)

        subprocess.run(
            ['git', '-C', repo_folder, 'fetch', '-a'],
            stderr=subprocess.STDOUT,
            stdout=open(os.devnull, 'w'))
