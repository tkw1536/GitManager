import typing
import os

from . import line
from ..repo import description as desc
from ..repo import implementation as impl


class Tree(object):
    """ Represents a Tree of Repositories """

    def __init__(self):
        """ Creates a new Tree object"""

        self.__lines = []

    @property
    def lines(self) -> typing.List[line.ConfigLine]:
        """ the lines currently contained in this File """
        return self.__lines

    @property
    def descriptions(self) -> \
            typing.Generator[typing.Tuple[int, desc.Description], None, None]:
        """ an iterator for pairs of (line, description) """

        # A stack for repo folders
        REPO_STACK = [os.path.expanduser('~')]

        for (i, l) in enumerate(self.lines):

            if isinstance(l, line.BaseLine):

                # extract the current and new order of the lines
                current_order = len(REPO_STACK)
                new_order = l.depth

                # we can not have a new order lower than 1 depth of the
                # current level
                if new_order > current_order:
                    raise Exception(
                        'Error in line {}: Missing base sublevel. '.format(
                            i + 1))

                # Read the sub-directory to be added and the old one
                sub_dir = os.path.expanduser(l.path)
                previous_item = REPO_STACK[new_order - 1]

                # add the new sub-directory
                new_sub_dir = os.path.join(previous_item, sub_dir)
                REPO_STACK[new_order:] = [new_sub_dir]

                # and yield it
                yield i, desc.BaseDescription(new_sub_dir)

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
                yield i, desc.RepositoryDescription(
                    source_uri, os.path.join(stack_loc, name))

    @property
    def repositories(self) -> typing.Generator[desc.RepositoryDescription,
                                               None, None]:
        """ an iterator for all repositories  """

        for (i, d) in self.descriptions:
            if isinstance(d, desc.RepositoryDescription):
                yield d

    @property
    def locals(self) -> typing.Generator[impl.LocalRepository, None,
                                         None]:
        """ an iterator for all localrepositories """

        for rd in self.repositories:
            yield rd.local

    @lines.setter
    def lines(self, ll: typing.List[line.ConfigLine]):
        """ sets the lines to be contained in this file """
        self.__lines = ll

    def find_base(self, path: str) -> typing.Optional[int]:
        """ Finds a specific base directory if it exists """
