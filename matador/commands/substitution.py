from .command import Command


class SubstituteKeywords(Command):

    def _execute(self):
        self._logger.info('SubstituteKeywords')


class CleanKeywords(Command):

    def _execute(self):
        self._logger.info('CleanKeywords')
