from matador.session import Session


def stage_file(file, repo=None):
    if repo is None:
        repo = Session.project_repo
    file_path = str(file.relative_to(repo.path))
    repo.stage(file_path)


def commit(message, repo=None):
    if repo is None:
        repo = Session.project_repo
    message = bytes(message, encoding='UTF-8')
    repo.do_commit(message)
