import typing

from ..repo import description
from . import Command


class Setup(Command):
    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """
        pass

    def run(self, repo: description.RepositoryDescription) -> bool:
        """ Sets up all repositories locally """
        if repo.local.exists():
            return True

        self.line.linebreak()
        return repo.remote.clone(repo.local)
