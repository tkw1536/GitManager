import collections
import os

from . import implementation
from abc import ABCMeta


class Description(metaclass=ABCMeta):
    """ A Base class for descriptions"""
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


@Description.register
class BaseDescription(collections.namedtuple("BaseDescription", ["folder"])):
    """ A 'description' of a base folder in the configuration file. """

    pass
