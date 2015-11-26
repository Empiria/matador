from .run_sql_script import RunSqlScript
from .deploy_ticket import DeployTicket, RemoveTicket
from .deploy_package import DeployPackage, RemovePackage
from .create_ticket import CreateTicket

commands = {
    'run-sql-script': RunSqlScript,
    'deploy-ticket': DeployTicket,
    'remove-ticket': RemoveTicket,
    'deploy-package': DeployPackage,
    'remove-package': RemovePackage,
    'create-ticket': CreateTicket
}
