from .run_sql_script import RunSqlScript
from .deploy_ticket import DeployTicket
from .substitution import SubstituteKeywords, CleanKeywords

commands = {
    'run-sql-script': RunSqlScript,
    'deploy-ticket': DeployTicket,
    'substitute-keywords': SubstituteKeywords,
    'clean-keywords': CleanKeywords
}
