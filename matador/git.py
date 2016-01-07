from dulwich.client import LocalGitClient


def stage_file(repo, file):
    file_path = str(file.relative_to(repo.path))
    repo.stage(file_path)


def commit(repo, message):
    message = bytes(message, encoding='UTF-8')
    repo.do_commit(message)


def fetch_all(source_repo, target_repo, remote_name=None):
    if remote_name is None:
        remote_name = 'origin'

    refs = LocalGitClient().fetch(source_repo.path, target_repo)

    for key, value in refs.items():
        key = key.replace(
            b'heads', b'remotes/%s' % bytes(remote_name, encoding='UTF-8'))
        target_repo.refs[key] = value
