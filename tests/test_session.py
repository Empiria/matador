import matador.session
from dulwich import porcelain
from pathlib import Path
from os import chdir
import pytest


@pytest.fixture
def repo_folder(tmpdir):
    repo_folder = Path(str(tmpdir), 'matador-test')
    if not repo_folder.is_dir():
        porcelain.init(str(repo_folder))
    return repo_folder


def test_project_folder(repo_folder):
    chdir(str(repo_folder))
    project_folder = matador.session.project_folder()
    assert project_folder == repo_folder
