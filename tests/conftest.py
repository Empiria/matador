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
        config_file = Path(repo_folder, '.git', 'config')
        config = repo.get_config()
        config.set(b'user', b'name', b'Test Example')
        config.set(b'user', b'email', b'test@example.org')
        config.write_to_path(str(config_file))
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

    commit = repo.do_commit(message=b'Create config files')

    repo.refs[b'refs/heads/master'] = commit
    repo.refs[b'refs/tags/test-tag'] = commit

    chdir(str(repo_folder))

    return repo
