from dulwich.repo import Repo
from dulwich.client import LocalGitClient
from pathlib import Path
from matador.session import Session
from globals import project, credentials, environments


def test_initialise(project_repo):
    Session.initialise()
    assert Session.project_folder == project_repo
    assert Session.project == project
    assert Session.matador_project_folder == Path(
        Path.home(), '.matador', project)
    assert Session.matador_repository_folder == Path(
        Path.home(), '.matador', project, 'repository')
    assert Session.environments == environments


def test_set_environment(project_repo):
    env = 'test'
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


def test_update_repository(project_repo):
    Session.update_repository()
    refs = LocalGitClient().get_refs(str(Session.matador_repository_folder))
    assert b'refs/remotes/origin/master' in refs
