from ..repo import description
from . import Command


class Pull(Command):
    """ Pulls a repository """

    LOCAL = True

    def run(self, repo: description.RepositoryDescription) -> bool:
        if not repo.local.exists():
            return False

        return repo.local.pull()
