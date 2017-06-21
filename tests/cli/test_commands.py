import os
from click.testing import CliRunner
import matador.cli.commands as cmd
import globals as gbl
from pathlib import Path


def test_init(tmpdir):
    project_folder = Path(str(tmpdir), gbl.project)
    os.chdir(tmpdir)
    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, ['init', '-p', gbl.project])

    result.exit_code == 0
    assert result.output == (
        f'Created matador project {gbl.project}\n')

    assert Path(project_folder, 'src').exists()


def test_create_ticket(project_repo):
    test_ticket = 'test-ticket'
    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, ['create-ticket', '--ticket', test_ticket])

    assert result.exit_code == 0
    assert result.output == f'Created ticket {test_ticket}\n'

    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')
    remove_file = Path(ticket_folder, 'remove.py')
    assert ticket_folder.exists()
    assert deploy_file.exists()
    assert remove_file.exists()

    last_commit = project_repo.get_object(project_repo.head())
    commit_message = last_commit.message
    expected_message = bytes(f'Create ticket {test_ticket}', encoding='UTF-8')
    assert commit_message == expected_message


def test_create_package(project_repo):
    test_package = 'test-package'
    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, ['create-package', '--package', test_package])

    assert result.exit_code == 0
    assert result.output == f'Created package {test_package}\n'

    package_folder = Path(
        project_repo.path, 'deploy', 'packages', test_package)
    package_file = Path(package_folder, 'tickets.yml')
    remove_file = Path(package_folder, 'remove.py')
    assert package_folder.exists()
    assert package_file.exists()
    assert remove_file.exists()

    last_commit = project_repo.get_object(project_repo.head())
    commit_message = last_commit.message
    expected_message = bytes(
        'Create package %s' % test_package, encoding='UTF-8')
    assert commit_message == expected_message


def test_add_ticket_to_package(project_repo):
    test_ticket = 'test-ticket'
    test_package = 'test-package'
    package_folder = Path(
        project_repo.path, 'deploy', 'packages', test_package)
    Path.mkdir(package_folder, parents=True)
    tickets_file = Path(package_folder, 'tickets.yml')
    tickets_file.touch()

    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, ['add-t2p', '-t', test_ticket, '-p', test_package])

    assert result.exit_code == 0
    assert result.output == (
        f'Added ticket {test_ticket} to package {test_package}\n')

    with tickets_file.open('r') as f:
        tickets = f.readlines()

    assert f'- {test_ticket}\n' in tickets


def test_deploy_ticket(project_repo):
    env = 'test'
    test_ticket = 'test-ticket'
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'deploy.py')

    ticket_folder.mkdir(parents=True)
    deploy_file.touch()
    with deploy_file.open('w') as f:
        f.write('import click\n\n')
        f.write('click.echo("Test Message")\n')

    deploy_path = str(deploy_file.relative_to(project_repo.path))
    project_repo.stage([bytes(deploy_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test ticket')

    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, [
            'deploy-ticket', '-e', env, '-t', test_ticket, '-c', 'HEAD'])

    assert result.exit_code == 0
    assert result.output == (
        f'Deploying ticket {test_ticket} to {env}\nTest Message\n')


def test_remove_ticket(project_repo):
    env = 'test'
    test_ticket = 'test-ticket'
    ticket_folder = Path(project_repo.path, 'deploy', 'tickets', test_ticket)
    deploy_file = Path(ticket_folder, 'remove.py')

    ticket_folder.mkdir(parents=True)
    deploy_file.touch()
    with deploy_file.open('w') as f:
        f.write('import click\n\n')
        f.write('click.echo("Test Message")\n')

    deploy_path = str(deploy_file.relative_to(project_repo.path))
    project_repo.stage([bytes(deploy_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test ticket')

    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, [
            'remove-ticket', '-e', env, '-t', test_ticket, '-c', 'HEAD'])

    assert result.exit_code == 0
    assert result.output == (
        f'Removing ticket {test_ticket} from {env}\nTest Message\n')


def test_deploy_package(project_repo):
    env = 'test'

    package = 'test_package'
    package_folder = Path(project_repo.path, 'deploy', 'packages', package)
    package_file = Path(package_folder, 'tickets.yml')
    package_folder.mkdir(parents=True)
    package_file.touch()

    for ticket in ('test-ticket-1', 'test-ticket-2'):
        ticket_folder = Path(project_repo.path, 'deploy', 'tickets', ticket)
        deploy_file = Path(ticket_folder, 'deploy.py')
        ticket_folder.mkdir(parents=True)
        deploy_file.touch()
        with deploy_file.open('w') as f:
            f.write('import click\n\n')
            f.write(f'click.echo("Test Message from {ticket}")\n')
        with package_file.open('a') as f:
            f.write(f'- {ticket}\n')
        ticket_path = str(deploy_file.relative_to(project_repo.path))
        project_repo.stage([bytes(ticket_path, encoding='UTF-8')])

    package_path = str(package_file.relative_to(project_repo.path))
    project_repo.stage([bytes(package_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test package')

    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, [
            'deploy-package', '-e', env, '-p', package, '-c', 'HEAD'])

    assert result.exit_code == 0
    expected_output = (
        f'Deploying package {package} to {env}\n'
        '*************************\n'
        f'Deploying ticket test-ticket-1 to {env}\n'
        'Test Message from test-ticket-1\n\n'
        '*************************\n'
        f'Deploying ticket test-ticket-2 to {env}\n'
        'Test Message from test-ticket-2\n\n'
        )
    assert result.output == expected_output


def test_remove_package(project_repo):
    env = 'test'

    package = 'test_package'
    package_folder = Path(project_repo.path, 'deploy', 'packages', package)
    package_file = Path(package_folder, 'tickets.yml')
    package_folder.mkdir(parents=True)
    package_file.touch()

    for ticket in ('test-ticket-1', 'test-ticket-2'):
        ticket_folder = Path(project_repo.path, 'deploy', 'tickets', ticket)
        deploy_file = Path(ticket_folder, 'deploy.py')
        ticket_folder.mkdir(parents=True)
        deploy_file.touch()
        with deploy_file.open('w') as f:
            f.write('import click\n\n')
            f.write(f'click.echo("Test Message from {ticket}")\n')
        with package_file.open('a') as f:
            f.write(f'- {ticket}\n')
        ticket_path = str(deploy_file.relative_to(project_repo.path))
        project_repo.stage([bytes(ticket_path, encoding='UTF-8')])

    package_path = str(package_file.relative_to(project_repo.path))
    project_repo.stage([bytes(package_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test package')

    runner = CliRunner()
    result = runner.invoke(
        cmd.matador, [
            'remove-package', '-e', env, '-p', package, '-c', 'HEAD'])

    assert result.exit_code == 0
    expected_output = (
        f'Removing package {package} from {env}\n'
        '*************************\n'
        f'Removing ticket test-ticket-1 from {env}\n'
        'Test Message from test-ticket-1\n\n'
        '*************************\n'
        f'Removing ticket test-ticket-2 from {env}\n'
        'Test Message from test-ticket-2\n\n'
        )
    assert result.output == expected_output
