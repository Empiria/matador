from .run_sql_script import RunSqlScript
from .deploy_ticket import DeployTicket

commands = {
    'run-sql-script': RunSqlScript,
    'deploy-ticket': DeployTicket,
}
