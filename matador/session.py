#!/usr/bin/env python
import logging
import yaml
from dulwich.repo import Repo
from dulwich.client import LocalGitClient
from dulwich.errors import NotGitRepository
from configparser import ConfigParser
from pathlib import Path

logger = logging.getLogger(__name__)


def get_environments(project_folder):
    """Fetch environment details from their config file."""
    file_path = Path(
        project_folder, 'config', 'environments.yml')
    try:
        file = file_path.open('r')
        environments = yaml.load(file)
        if environments:
            return environments
        else:
            raise ValueError()
    except FileNotFoundError:
        logger.error('Cannot find environments.yml file')
    except ValueError:
        logger.error('environments.yml exists but is empty')


def get_credentials(project_folder):
    """Fetch credential details from their config file."""
    file_path = Path(
        project_folder, 'config', 'credentials.yml')
    try:
        file = file_path.open('r')
        credentials = yaml.load(file)
        if credentials:
            return credentials
        else:
            raise ValueError()
    except FileNotFoundError:
        logger.error('Cannot find credentials.yml file')
    except ValueError:
        logger.error('credentials.yml exists but is empty')


def initialise_repository(proj_folder, repo_folder):
    """Create a git repository for matador to use."""
    config_file = Path(repo_folder, '.git', 'config')
    config = ConfigParser()

    repo = Repo.init(str(repo_folder))
    config.read(str(config_file))

    config['core']['sparsecheckout'] = 'true'
    config['remote "origin"'] = {
        'url': proj_folder,
        'fetch': '+refs/heads/*:refs/remotes/origin/*'
    }

    with config_file.open('w') as f:
        config.write(f)
        f.close()

    sparse_checkout_file = Path(
        repo_folder, '.git', 'info', 'sparse-checkout')
    with sparse_checkout_file.open('a') as f:
        f.write('/src\n')
        f.write('/deploy\n')
        f.close()

    return repo


class Session(object):

    """A class to hold variables for a matador session."""

    project_folder = None
    environment = None

    @classmethod
    def initialise(self):
        """Set the project name and folders for its repositories."""
        if self.project_folder is not None:
            return
        else:
            self.project_repo = Repo.discover()
            self.project_folder = Path(self.project_repo.path)

            self.project = self.project_folder.name

            self.matador_project_folder = Path(
                Path.home(), '.matador', self.project)

            self.matador_repository_folder = Path(
                self.matador_project_folder, 'repository')

            self.environments = get_environments(self.project_folder)

    @classmethod
    def _initialise_matador_repository(self):
        """Initialise a git repository for matador to use."""
        Path.mkdir(
            self.matador_project_folder, parents=True, exist_ok=True)
        Path.mkdir(
            self.matador_repository_folder, parents=True, exist_ok=True)

        try:
            repo = Repo(str(self.matador_repository_folder))
        except NotGitRepository:
            repo = initialise_repository(
                self.project_folder, self.matador_repository_folder)
        return repo

    @classmethod
    def set_environment(self, environment):
        """Set a specific environment for those commands which require it."""

        if self.project_folder is None:
            self.initialise()

        if self.environment is not None:
            return
        else:
            self._initialise_matador_repository()
            self.environment = self.environments[environment]
            credentials = get_credentials(self.project_folder)
            self.credentials = credentials[environment]

            self.matador_environment_folder = Path(
                self.matador_project_folder, environment)
            self.matador_tickets_folder = Path(
                self.matador_environment_folder, 'tickets')
            self.matador_packages_folder = Path(
                self.matador_environment_folder, 'packages')

            Path.mkdir(
                self.matador_environment_folder, parents=True, exist_ok=True)
            Path.mkdir(
                self.matador_tickets_folder, parents=True, exist_ok=True)
            Path.mkdir(
                self.matador_packages_folder, parents=True, exist_ok=True)

    @classmethod
    def update_repository(self):
        """Fetch all from the project repo to the matador repo."""

        if self.project_folder is None:
            self.initialise()

        try:
            repo = Repo(str(self.matador_repository_folder))
        except NotGitRepository:
            repo = self._initialise_matador_repository()

        refs = LocalGitClient().fetch(str(self.project_folder), repo)

        for key, value in refs.items():
            key = key.replace(b'heads', b'remotes/origin')
            repo.refs[key] = value

    @classmethod
    def clear(self):
        self.project_folder = None
        self.environment = None
