import globals as gbl
from matador.commands import CreateTicket, CreatePackage
from dulwich.repo import Repo


def test_add_to_git(project_repo):
    pass


def test_create_ticket(project_repo):
    CreateTicket(ticket='test-ticket')


def test_create_package(project_repo):
    CreatePackage(package='test-package')
