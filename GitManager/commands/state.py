import typing
import argparse

from ..repo import description
from ..repo import implementation
from ..utils import format
from . import Command


class State(Command):
    """ Checks the state of all repositories, and list all those out-of-date"""
    LOCAL = True
    FILTER = True

    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """
        parser = argparse.ArgumentParser(prog='git-manager state')
        parser.add_argument('pattern', nargs='?')

        group = parser.add_mutually_exclusive_group()
        group.add_argument('--update', dest='update',
                           action='store_true', default=True,
                           help='Update remote references using \'git '
                                'remote update\' before showing status. '
                                'Enabled by default.  ')
        group.add_argument('--no-update', dest='update',
                           action='store_false',
                           help='DO NOT update remote references using '
                                '\'git remote update\' '
                                'before showing status. ')

        targs = parser.parse_args(args)
        if targs.pattern:
            super(State, self).parse(targs.pattern)

        return targs

    def run(self, repo: description.RepositoryDescription) -> bool:

        if not repo.local.exists():
            return False

        status = repo.local.remote_status(self.args.update)

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
