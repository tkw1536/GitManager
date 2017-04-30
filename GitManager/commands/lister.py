import typing

from ..repo import description
from . import Command


class LsLocal(Command):
    """ Lists all local commands """

    PLAIN = True
    LOCAL = True

    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """
        pass

    def run(self, repo: description.RepositoryDescription) -> bool:
        if repo.local.exists():
            print(repo.local.path)

        return True
