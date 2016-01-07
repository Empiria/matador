import pytest
from pathlib import Path
from shutil import rmtree
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo
import yaml
from os import chdir
from matador.session import Session
from globals import project, credentials, environments


@pytest.fixture
def session(request):

    def finalise():
        Session.clear()
    request.addfinalizer(finalise)


@pytest.fixture
def repo(tmpdir, request):
    repo_folder = Path(str(tmpdir), project)
    try:
        repo = Repo(str(repo_folder))
    except NotGitRepository:
        repo = Repo.init(str(repo_folder), mkdir=True)
    return repo


@pytest.fixture
def project_repo(tmpdir, request, repo, session):
    repo_folder = Path(repo.path)

    def finalise():
        rmtree(
            str(Path(Path.home(), '.matador', project)), ignore_errors=True)

    request.addfinalizer(finalise)

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

    chdir(str(repo_folder))

    return repo_folder
