import logging


class DeploymentCommand(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._execute()

    def _execute(self):
        raise NotImplementedError
