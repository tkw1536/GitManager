import collections
import os

from . import implementation


class RepositoryDescription(collections.namedtuple("RepositoryDescription",
                                                   ["source", "path"])):
    """ A 'description' of a repository, i.e. a pair of source and path """

    @property
    def local(self) -> implementation.LocalRepository:
        return implementation.LocalRepository(self.path)

    @property
    def remote(self) -> implementation.RemoteRepository:
        """ the remote repository described by this RepositoryDescription """
        return implementation.RemoteRepository(self.source)
