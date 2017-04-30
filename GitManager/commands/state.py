import typing

from ..repo import description
from ..repo import implementation
from ..utils import format
from . import Command


class State(Command):
    """ Checks the state of all repositories, and list all those out-of-date"""
    LOCAL = True

    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """
        pass

    def run(self, repo: description.RepositoryDescription) -> bool:

        if not repo.local.exists():
            return False

        status = repo.local.remote_status()

        if status == implementation.RemoteStatus.REMOTE_NEWER:
            self.line.linebreak()
            print(format.Format.yellow('Upstream is ahead of your branch, '
                                       'pull required. '))

        elif status == implementation.RemoteStatus.LOCAL_NEWER:
            self.line.linebreak()
            print(format.Format.green('Your branch is ahead of upstream, '
                                      'push required.'))
        elif status == implementation.RemoteStatus.DIVERGENCE:
            self.line.linebreak()
            print(format.Format.red('Your branch and upstream have diverged, '
                                    'merge or rebase required. '))

        return status == implementation.RemoteStatus.UP_TO_DATE
