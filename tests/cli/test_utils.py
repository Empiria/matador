from pathlib import Path
import globals as gbl
import matador.cli.utils as utils


def test_repository(project_repo):
    project_folder = Path(project_repo.path)
    deployment_folder = Path(Path.home(), '.matador', gbl.project)
    deployment_repo_folder = Path(deployment_folder, 'repository')
    utils.deployment_repository(project_folder)

    assert deployment_repo_folder.exists()
    assert Path(
        deployment_repo_folder, '.git', 'info', 'sparse-checkout').exists()


def test_ticket_deployment_folder(project_repo):
    env = 'test'
    test_ticket = 'test-ticket'
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')

    ticket_folder.mkdir(parents=True)
    deploy_file.touch()

    deploy_path = str(deploy_file.relative_to(project_repo.path))
    project_repo.stage([bytes(deploy_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test ticket')

    utils.ticket_deployment_folder(env, test_ticket, 'HEAD', False)

    checked_out_file = Path(
        Path.home(), '.matador', gbl.project, env, 'tickets', test_ticket,
        'deploy.py')
    assert checked_out_file.exists()


def test_package_definition(project_repo):
    env = 'test'

    package = 'test_package'
    package_folder = Path(project_repo.path, 'deploy', 'packages', package)
    package_file = Path(package_folder, 'tickets.yml')
    package_folder.mkdir(parents=True)
    package_file.touch()

    with package_file.open('w') as f:
        f.write(f'- test_ticket_1\n')
        f.write(f'- test_ticket_2\n')

    package_path = str(package_file.relative_to(project_repo.path))
    project_repo.stage([
        bytes(package_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test package')

    tickets_file = utils.package_definition(env, package, 'HEAD')

    deployment_folder = Path(
        Path.home(), '.matador', gbl.project, env, 'packages', package)
    assert tickets_file.parent == deployment_folder
