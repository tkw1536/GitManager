import typing

from ..repo import description
from . import Command


class GC(Command):
    """ Runs house keeping tasks with parameters """

    LOCAL = True

    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """
        self.__args = args

    def run(self, repo: description.RepositoryDescription) -> bool:
        if not repo.local.exists():
            return False

        self.line.linebreak()
        return repo.local.gc(*self.__args)
