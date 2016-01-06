import matador.commands.create as cmd
from matador.session import Session
from dulwich.repo import Repo
from dulwich.diff_tree import tree_changes
from pathlib import Path


def test_stage_file(project_repo):
    Session.initialise()
    test_file = Path(project_repo, 'test_file')
    test_file.touch()
    cmd.stage_file(test_file)

    repo = Repo(str(project_repo))
    index = repo.open_index()
    changes = [f.decode('UTF-8') for f in index]

    assert str(test_file) in changes


def test_commit(project_repo):
    Session.initialise()
    test_file = Path(project_repo, 'test_file')
    test_file.touch()
    message = b'Test commit\n'
    repo = Repo(str(project_repo))
    repo.stage([str(test_file)])

    cmd.commit(message)

    last_commit = repo.get_object(repo.head())
    commit_message = last_commit.message
    assert commit_message == message


def test_create_ticket(project_repo):
    test_ticket = 'test-ticket'
    cmd.CreateTicket(ticket=test_ticket)

    ticket_folder = Path(project_repo, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')
    assert ticket_folder.exists()
    assert deploy_file.exists()

    repo = Repo(str(project_repo))
    last_commit = repo.get_object(repo.head())
    commit_message = last_commit.message
    expected_message = bytes(
        'Create ticket %s\n' % test_ticket, encoding='UTF-8')
    assert commit_message == expected_message


def test_create_package(project_repo):
    test_package = 'test-package'
    cmd.CreatePackage(package=test_package)

    package_folder = Path(project_repo, 'deploy', 'packages', test_package)
    package_file = Path(package_folder, 'tickets.yml')
    remove_file = Path(package_folder, 'remove.py')
    assert package_folder.exists()
    assert package_file.exists()
    assert remove_file.exists()

    repo = Repo(str(project_repo))
    last_commit = repo.get_object(repo.head())
    commit_message = last_commit.message
    expected_message = bytes(
        'Create package %s\n' % test_package, encoding='UTF-8')
    assert commit_message == expected_message


def test_add_ticket_to_package(project_repo):
    assert 'Not Implemented' is True
