import matador.commands as cmd
import globals as gbl
from pathlib import Path


def test_deploy_ticket(project_repo):
    env = 'test'
    test_ticket = 'test-ticket'
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')

    ticket_folder.mkdir(parents=True)
    deploy_file.touch()

    deploy_path = str(deploy_file.relative_to(project_repo.path))
    project_repo.stage([bytes(deploy_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test ticket')

    cmd.DeployTicket(environment=env, ticket=test_ticket, commit='HEAD')

    checked_out_file = Path(
        Path.home(), '.matador', gbl.project, env, 'tickets', test_ticket,
        'deploy.py')
    assert checked_out_file.exists()
