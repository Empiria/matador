from matador.session import Session
from dulwich import porcelain
from dulwich.repo import Repo
from pathlib import Path
from os import chdir
import pytest
import yaml

environments = {
    'test': {'dbms': 'oracle', 'connection': 'user@instance'}
}

credentials = {
    'test': {'user': 'test_user', 'password': 'test_password'}
}

@pytest.fixture
def repo_folder(tmpdir):
    repo_folder = Path(str(tmpdir), 'matador-test')
    if not repo_folder.is_dir():
        porcelain.init(str(repo_folder))
    return repo_folder


@pytest.fixture
def config_files(repo_folder):
    config_folder = Path(repo_folder, 'config')
    config_folder.mkdir()
    with Path(config_folder, 'environments.yml') as f:
        f.touch()
        f.open(mode='w')
        f.write_text(yaml.dump(environments))
    with Path(config_folder, 'credentials.yml') as f:
        f.touch()
        f.open(mode='w')
        f.write_text(yaml.dump(credentials))


def test_initialise_session(repo_folder, config_files):
    project = 'matador-test'
    chdir(str(repo_folder))
    Session.initialise_session()
    assert Session.project_folder == repo_folder
    assert Session.project == project
    assert Session.matador_project_folder == Path(
        Path.home(), '.matador', project)
    assert Session.matador_repository_folder == Path(
        Path.home(), '.matador', project, 'repository')
    assert Session.environments == environments


def test_set_environment(repo_folder):
    project = 'matador-test'
    env = 'test'
    chdir(str(repo_folder))
    Session.initialise_session()
    Session.set_environment(env)
    assert Session.matador_project_folder.is_dir()
    assert Session.matador_repository_folder.is_dir()
    assert Repo(str(Session.matador_repository_folder)).has_index()
    assert Session.environment == environments[env]
    assert Session.credentials == credentials[env]
    assert Session.matador_environment_folder == Path(
        Path.home(), '.matador', project, env)
    assert Session.matador_tickets_folder == Path(
        Path.home(), '.matador', project, env, 'tickets')
    assert Session.matador_packages_folder == Path(
        Path.home(), '.matador', project, env, 'packages')
    assert Session.matador_environment_folder.is_dir()
    assert Session.matador_tickets_folder.is_dir()
    assert Session.matador_packages_folder.is_dir()


def test_update_repository():
    Session.update_repository()

