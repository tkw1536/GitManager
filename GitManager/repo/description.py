import collections
import os
import typing

from . import implementation
from ..config import line
from abc import ABCMeta


class Description(metaclass=ABCMeta):
    """ A Base class for descriptions"""
    pass


@Description.register
class BaseDescription(collections.namedtuple("BaseDescription", ["folder"])):
    """ A 'description' of a base folder in the configuration file. """

    pass


@Description.register
class RepositoryDescription(collections.namedtuple("RepositoryDescription",
                                                   ["source", "path"])):
    """A 'description' of a repository in the configuration file, i.e. a
    a pair of (source, path) """

    @property
    def local(self) -> implementation.LocalRepository:
        """ Gets the local repository associated to this
        RepositoryDescription """
        return implementation.LocalRepository(self.path)

    @property
    def remote(self) -> implementation.RemoteRepository:
        """ Gets the remote repository associated to this
        RepositoryDescription """
        return implementation.RemoteRepository(self.source)

    def to_repo_line(self, indent: str, space_1: str, space_2: str) -> \
            typing.Tuple[BaseDescription, line.RepoLine]:
        """ Turns this RepositoryDescription into an appropriate RepoLine
        and description. """

        # get the base name and git clone name
        (base, name) = os.path.split(self.path)
        git_name = self.remote.humanish_part()

        # if the git name is identical to the already existing name, we just
        # give the source
        if name == git_name:
            return BaseDescription(base), line.RepoLine(indent, self.source,
                                                        '', '', space_2)

        # else we need to give both
        else:
            return BaseDescription(base), line.RepoLine(indent, self.source,
                                                        space_1, name, space_2)
