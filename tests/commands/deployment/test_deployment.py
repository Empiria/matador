from matador.commands.deployment.deployment import substitute_keywords
from time import strftime, gmtime
from dulwich.objects import format_timezone


def test_substitute_keywords(project_repo):
    test_text = """\
        First line
        version:
        date:
        Last line"""

    commit = project_repo.get_object(project_repo.head())
    commit_time = strftime('%Y-%m-%d %H:%M:%S', gmtime(commit.commit_time))
    timezone = format_timezone(commit.commit_timezone).decode(encoding='ascii')
    commit_timestamp = commit_time + ' ' + timezone

    expected_result = """\
        First line
        version: HEAD
        date: %s
        Last line""" % commit_timestamp

    result = substitute_keywords(
        test_text, project_repo.path, 'HEAD')
    assert result == expected_result
