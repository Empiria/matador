import matador.commands as cmd
import globals as gbl
from pathlib import Path


def test_deploy_package(project_repo):
    env = 'test'

    ticket_1 = 'test-ticket-1'
    ticket_1_folder = Path(project_repo.path, 'deploy', 'tickets', ticket_1)
    deploy_file_1 = Path(ticket_1_folder, 'deploy.py')
    ticket_1_folder.mkdir(parents=True)
    deploy_file_1.touch()

    ticket_2 = 'test-ticket-2'
    ticket_2_folder = Path(project_repo.path, 'deploy', 'tickets', ticket_2)
    deploy_file_2 = Path(ticket_2_folder, 'deploy.py')
    ticket_2_folder.mkdir(parents=True)
    deploy_file_2.touch()

    package = 'test_package'
    package_folder = Path(project_repo.path, 'deploy', 'packages', package)
    package_file = Path(package_folder, 'tickets.yml')
    package_folder.mkdir(parents=True)
    package_file.touch()

    with package_file.open('w') as f:
        f.write('- %s\n' % ticket_1)
        f.write('- %s\n' % ticket_2)
        f.close()

    ticket_1_path = str(deploy_file_1.relative_to(project_repo.path))
    ticket_2_path = str(deploy_file_2.relative_to(project_repo.path))
    package_path = str(package_file.relative_to(project_repo.path))
    project_repo.stage([
        bytes(ticket_1_path, encoding='UTF-8'),
        bytes(ticket_2_path, encoding='UTF-8'),
        bytes(package_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test package')

    cmd.DeployPackage(environment=env, package=package, commit='HEAD')

    ticket_file_1 = Path(
        Path.home(), '.matador', gbl.project, env, 'tickets', ticket_1,
        'deploy.py')
    ticket_file_2 = Path(
        Path.home(), '.matador', gbl.project, env, 'tickets', ticket_2,
        'deploy.py')
    checked_out_file = Path(
        Path.home(), '.matador', gbl.project, env, 'packages', package,
        'tickets.yml')
    assert ticket_file_1.exists()
    assert ticket_file_2.exists()
    assert checked_out_file.exists()
