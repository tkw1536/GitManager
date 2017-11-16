import typing

from ..repo import description
from . import Command


class Pull(Command):
    """ Pulls a repository """

    LOCAL = True
    FILTER = True

    def run(self, repo: description.RepositoryDescription) -> bool:
        if not repo.local.exists():
            return False

        self.line.linebreak()
        return repo.local.pull()
