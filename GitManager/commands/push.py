import typing

from ..repo import description
from . import Command


class Push(Command):
    """ Pushes a repository """

    LOCAL = True

    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """
        pass

    def run(self, repo: description.RepositoryDescription) -> bool:
        if not repo.local.exists():
            return False

        self.line.linebreak()
        return repo.local.push()
