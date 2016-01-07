import matador.commands as cmd
from pathlib import Path


def test_deploy_ticket(project_repo):
    test_ticket = 'test-ticket'
    ticket_folder = Path(project_repo, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')

    ticket_folder.mkdir(parents=True)
    deploy_file.touch()

    cmd.DeployTicket(environment='test', ticket=test_ticket, commit='HEAD')
