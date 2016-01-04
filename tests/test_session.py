from matador.session import Session
from dulwich.repo import Repo
from dulwich.client import LocalGitClient
from dulwich.objects import Blob, Tree, Commit, parse_timezone
from dulwich.errors import NotGitRepository
from time import time
from pathlib import Path
import shutil
from os import chdir
import pytest
import yaml

project = 'matador-test'

environments = {
    'test': {'dbms': 'oracle', 'connection': 'user@instance'}
}

credentials = {
    'test': {'user': 'test_user', 'password': 'test_password'}
}


@pytest.fixture
def project_repo(tmpdir, request):

    def finalise():
        shutil.rmtree(
            str(Path(Path.home(), '.matador', project)), ignore_errors=True)

    request.addfinalizer(finalise)

    repo_folder = Path(str(tmpdir), project)
    try:
        repo = Repo(str(repo_folder))
    except NotGitRepository:
        repo = Repo.init(str(repo_folder), mkdir=True)

    config_folder = Path(repo_folder, 'config')
    config_folder.mkdir()

    envs_file = Path(config_folder, 'environments.yml')
    creds_file = Path(config_folder, 'credentials.yml')

    with envs_file as f:
        f.touch()
        f.write_text(yaml.dump(environments))

    with creds_file as f:
        f.touch()
        f.write_text(yaml.dump(credentials))

    repo.stage([
        bytes(str(envs_file.relative_to(repo_folder)), encoding='UTF-8'),
        bytes(str(creds_file.relative_to(repo_folder)), encoding='UTF-8')
    ])

    repo.do_commit(message=b'Create config files')

    return repo_folder


def test_initialise_session(project_repo):
    chdir(str(project_repo))
    Session.initialise_session()
    assert Session.project_folder == project_repo
    assert Session.project == project
    assert Session.matador_project_folder == Path(
        Path.home(), '.matador', project)
    assert Session.matador_repository_folder == Path(
        Path.home(), '.matador', project, 'repository')
    assert Session.environments == environments


def test_set_environment(project_repo):
    env = 'test'
    chdir(str(project_repo))
    Session.initialise_session()
    Session.set_environment(env)
    config = Repo(str(Session.matador_repository_folder)).get_config()
    assert config.get(b'core', b'sparsecheckout') == b'true'
    assert Session.matador_project_folder.is_dir()
    assert Session.matador_repository_folder.is_dir()
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
    refs = LocalGitClient().get_refs(str(Session.matador_repository_folder))
    assert b'refs/remotes/origin/master' in refs
