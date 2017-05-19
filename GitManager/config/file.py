import typing
import os.path

from . import line, tree


class File(tree.Tree):
    """ Methods for parsing and reading configuration file. """

    def __init__(self, fn: str):
        """ Creates a new File object"""

        super().__init__()

        self.__fn = fn

    def read(self):
        """ Re-reads the lines currently contained in this file """

        with open(self.__fn, "r") as fp:
            self.lines = [line.ConfigLine.parse(l.rstrip('\n')) for l in
                          fp.readlines()]

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
