from dulwich.client import LocalGitClient
from dulwich.index import build_index_from_tree


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


def checkout(repo, ref=None):
    if ref is None:
        ref = 'HEAD'
    index = repo.index_path()
    tree_id = repo[ref].tree
    build_index_from_tree(repo.path, index, repo.object_store, tree_id)
