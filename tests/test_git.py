from matador import git
from pathlib import Path


def test_stage_file(repo):
    repo_folder = Path(repo.path)
    test_file = Path(repo_folder, 'test_file')
    test_file.touch()
    git.stage_file(repo, test_file)

    index = repo.open_index()
    changes = [f.decode('UTF-8') for f in index]

    assert str(test_file.relative_to(repo_folder)) in changes


def test_commit(repo):
    repo_folder = Path(repo.path)
    test_file = Path(repo_folder, 'test_file')
    test_file.touch()
    message = 'Test commit'
    repo.stage([str(test_file.relative_to(repo_folder))])

    git.commit(repo, message)

    last_commit = repo.get_object(repo.head())
    commit_message = last_commit.message
    assert commit_message == bytes(message, encoding='UTF-8')
