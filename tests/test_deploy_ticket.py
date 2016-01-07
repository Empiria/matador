import matador.commands as cmd
from pathlib import Path


def test_deploy_ticket(project_repo):
    test_ticket = 'test-ticket'
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')

    ticket_folder.mkdir(parents=True)
    deploy_file.touch()

    deploy_path = str(deploy_file.relative_to(project_repo.path))
    project_repo.stage([bytes(deploy_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test ticket')

    cmd.DeployTicket(environment='test', ticket=test_ticket, commit='HEAD')
