import typing

from ..repo import description
from ..utils import run
from . import Command


class Status(Command):
    """ Checks that status of all repositories """
    LOCAL = True
    FILTER = True

    def run(self, repo: description.RepositoryDescription) -> bool:

        if not repo.local.exists():
            return False

        status = repo.local.local_status()

        if status is not None and status != '':
            self.line.linebreak()
            run.GitRun("status", cwd=repo.local.path, pipe_stdout=True).wait()

        return status == ''
