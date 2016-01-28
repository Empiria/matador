from matador.commands.deployment import deploy_sql_script
from pathlib import Path


def test_checkout_script(project_repo):
    test_script = Path(project_repo.path, 'test-script')
    test_script.touch()

    stage_path = str(test_script.relative_to(project_repo.path))
    project_repo.stage([bytes(stage_path, encoding='UTF-8')])
    project_repo.do_commit(message=b'Create test script')

    checked_out_path = deploy_sql_script._checkout_script(
        stage_path, project_repo.head().decode())

