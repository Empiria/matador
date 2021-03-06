import matador.cli.sql as sql


def test_command_condition():
    assert sql.command_condition(True, True, True, True) == ('command')
    assert sql.command_condition(True, False, True, True) == ('command')
    assert sql.command_condition(True, True, False, True) == ('command')
    assert sql.command_condition(True, True, True, False) == ('command')

    assert sql.command_condition(False, True, True, True) == ('oracle')
    assert sql.command_condition(False, True, False, True) == ('oracle')
    assert sql.command_condition(False, True, True, False) == ('oracle')

    assert sql.command_condition(False, False, True, True) == (
        'mssql', 'posix')
    assert sql.command_condition(False, False, True, False) == (
        'mssql', 'posix')

    assert sql.command_condition(False, False, False, True) == (
        'mssql', 'nt', 'windows_authentication')

    assert sql.command_condition(False, False, False, False) == (
        'mssql', 'nt', 'mssql_authentication')


def test_command():
    command = sql.command(
        command='test command',
        dbms='oracle',
        client_os='posix',
        server='test_server',
        db_name='test_db',
        user='uid',
        password='pwd')
    assert command == 'test command'

    command = sql.command(
        dbms='oracle',
        client_os='posix',
        server='test_server',
        db_name='test_db',
        port='test_port',
        user='uid',
        password='pwd')
    assert command == 'sqlplus -S -L uid/pwd@test_server:test_port/test_db'

    command = sql.command(
        dbms='mssql',
        client_os='posix',
        server='test_server',
        db_name='test_db',
        user='uid',
        password='pwd')
    assert command == 'bsqldb -S test_server -D test_db -U uid -P pwd'

    command = sql.command(
        dbms='mssql',
        client_os='nt',
        server='test_server',
        db_name='test_db',
        windows_authentication=True)
    assert command == 'sqlcmd -S test_server -d test_db -E'

    command = sql.command(
        dbms='mssql',
        client_os='nt',
        server='test_server',
        db_name='test_db',
        user='uid',
        password='pwd')
    assert command == 'sqlcmd -S test_server -d test_db -U uid -P pwd'
