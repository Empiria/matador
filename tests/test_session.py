from matador.session import Session, project_folder
from dulwich import porcelain
from pathlib import Path
from os import chdir
import pytest
import yaml

environments = {
    'test': {'dbms': 'oracle', 'connection': 'user@instance'}
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
    Path(config_folder, 'credentials.yml').touch()


def test_project_folder(repo_folder):
    chdir(str(repo_folder))
    assert project_folder() == repo_folder


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
