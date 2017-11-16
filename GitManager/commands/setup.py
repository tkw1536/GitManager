import typing

from ..repo import description
from . import Command


class Setup(Command):

    FILTER = True

    def run(self, repo: description.RepositoryDescription) -> bool:
        """ Sets up all repositories locally """
        if repo.local.exists():
            return True

        self.line.linebreak()
        return repo.remote.clone(repo.local)
