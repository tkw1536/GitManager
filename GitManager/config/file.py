import re
import os.path

import typing

from . import line
from ..repo import description as desc
from ..repo import implementation as impl


class File(object):
    """ Methods for parsing and reading configuration file. """

    def __init__(self, fn: str):
        """ Creates a new File object"""

        self.__fn = fn
        self.__lines = []

    @property
    def lines(self) -> typing.List[line.ConfigLine]:
        """ the lines currently contained in this File """
        return self.__lines

    @property
    def descriptions(self) -> typing.Generator[desc.RepositoryDescription,
                                               None, None]:
        """ returns a list of named """

        # A stack for repo folders
        REPO_STACK = [os.path.expanduser('~')]

        for l in self.lines:

            if isinstance(l, line.NOPLine):
                pass

            if isinstance(l, line.BaseLine):

                # extract the current and new order of the lines
                current_order = len(REPO_STACK)
                new_order = l.depth

                # we can not have a new order lower than 1 depth of the
                # current level
                if new_order > current_order:
                    raise Exception(
                        'Unable to parse config file: Missing base sublevel. ')

                # Read the sub-directory to be added and the old one
                sub_dir = os.path.expanduser(l.path)
                previous_item = REPO_STACK[new_order - 1]

                # add the new sub-directory
                new_sub_dir = os.path.join(previous_item, sub_dir)
                REPO_STACK[new_order:] = [new_sub_dir]

            if isinstance(l, line.RepoLine):
                # Extract the base directory and the source url
                stack_loc = REPO_STACK[-1]
                source_uri = l.url

                # And the path to clone to
                folder = os.path.expanduser(l.path) or None
                path = os.path.join(stack_loc, folder) \
                    if folder is not None else None

                name = path if path is not None else \
                    impl.RemoteRepository(source_uri).humanish_part()

                # and yield the actual repository
                yield desc.RepositoryDescription(source_uri,
                                                 os.path.join(stack_loc, name),
                                                 )

    @property
    def locals(self) -> typing.Generator[impl.LocalRepository, None,
                                         None]:
        """ Iterates over a list of local repositories """

        for desc in self.descriptions:
            yield desc.local

    @lines.setter
    def lines(self, ll: typing.List[line.ConfigLine]):
        """ sets the lines to be contained in this file """
        self.__lines = ll

    def read(self):
        """ Re-reads the lines currently contained in this file """

        with open(self.__fn, "r") as fp:
            self.__lines = [line.ConfigLine.parse(l) for l in fp.readlines()]

    def write(self):
        """ Writes the lines currently contained in this file to disk """

        with open(self.__fn, "w") as fp:
            for l in self.lines:
                fp.write("{}\n".format(l.write()))

    @staticmethod
    def find() -> typing.Optional[str]:
        """finds the location of the configuration file"""

        # 1. Check $GIT_MANAGER_CONFIG if set
        if "GIT_MANAGER_CONFIG" in os.environ:
            git_manager_config = os.environ["GIT_MANAGER_CONFIG"]

            if os.path.isfile(git_manager_config):
                return git_manager_config

        # 2. ~/.config/.gitmanager/config
        # (or $XDG_CONFIG_HOME/.gitmanager/config if set)
        if "XDG_CONFIG_HOME" in os.environ:
            xdg_config_home = os.environ["XDG_CONFIG_HOME"]
        else:
            xdg_config_home = os.path.join(os.path.expanduser("~"), ".config")

        xdg_config_path = os.path.join(xdg_config_home, ".gitmanager",
                                       "config")
        if os.path.isfile(xdg_config_path):
            return xdg_config_path

        # 3. ~/.gitmanager
        fallback_path = os.path.join(os.path.expanduser("~"), ".gitmanager")
        if os.path.isfile(fallback_path):
            return fallback_path


__all__ = ["File"]
