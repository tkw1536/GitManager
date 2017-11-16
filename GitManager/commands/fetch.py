import typing

from ..repo import description
from . import Command


class Fetch(Command):
    """ Fetch all remotes for all repositories """

    LOCAL = True
    FILTER = True

    def run(self, repo: description.RepositoryDescription) -> bool:
        if not repo.local.exists():
            return False

        return repo.local.fetch()
