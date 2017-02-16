from typing import List

import typing

from ..utils import format
from ..repo import description


class Command(object):
    """ Flag indicating if this command is a plain command, that is not
    fancy lines will be used. """
    PLAIN = False
    LOCAL = False

    def __init__(self, line: format.TerminalLine,
                 repos: List[description.RepositoryDescription]):
        self.__line = line
        self.__repos = repos

        # current state when running this command
        self.__idx = None
        self.__repo = None

    @property
    def repos(self) -> List[description.RepositoryDescription]:
        """ A list of repositories subject to this command. """

        # if we are a local command, we only use local repositories
        if self.__class__.LOCAL:
            return list(filter(lambda ds: ds.local.exists(), self.__repos))

        # else we return all the repositories
        else:
            return list(self.__repos)

    @property
    def line(self) -> format.TerminalLine:
        return self.__line

    def run(self, repo: description.RepositoryDescription) -> bool:
        """ Runs this Command on a given repository """

        raise NotImplementedError

    def write(self, message: typing.Any):
        """ Writes text from this command. """
        self.line.linebreak()
        print(message)

    def write_with_counter(self, message: str):
        """ Writes a message together with a counter into the line """

        # repo count and number of zeros for it
        repo_count = len(self.repos)
        zcount = len(str(repo_count))

        # the prefix - a counter
        prefix = "[{}/{}] ".format(
            str(self.__idx + 1).zfill(zcount),
            repo_count,
        )

        self.line.write("{}{}".format(prefix, message))

    def write_path_with_counter(self, path: str):
        """ Writes a path with a counter"""

        # repo count and number of zeros for it
        repo_count = len(self.repos)
        zcount = len(str(repo_count))

        # the prefix - a counter
        prefix = "[{}/{}] ".format(
            str(self.__idx + 1).zfill(zcount),
            repo_count,
        )

        # and write the message to the output
        message = format.Format.short_path(path, self.line.width - len(prefix))
        self.write_with_counter(message)

    def __call__(self) -> int:
        counter = 0
        for (i, repo) in enumerate(self.repos):
            self.__idx = i
            self.__repo = repo

            if not self.__class__.PLAIN:
                self.write_path_with_counter(repo.local.path)

            if self.run(repo):
                counter += 1

        self.line.clean()

        return counter
