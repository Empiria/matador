from matador.commands.create import add_to_git, CreateTicket, CreatePackage
from dulwich.repo import Repo
from pathlib import Path


def test_add_to_git(project_repo):
    Path(project_repo, 'test_file').touch()
    message = b'Test commit\n'
    add_to_git(project_repo, message)

    repo = Repo(str(project_repo))
    last_commit = repo.get_object(repo.head())
    commit_message = last_commit.message
    assert commit_message == message


def test_create_ticket(project_repo):
    test_ticket = 'test-ticket'
    CreateTicket(ticket=test_ticket)

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
    CreatePackage(package=test_package)

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
