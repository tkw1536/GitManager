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
        self.__base_directory = os.path.expanduser('~').rstrip("/")
        self.__root = self.__base_directory

    @property
    def lines(self) -> typing.List[line.ConfigLine]:
        """ the lines currently contained in this File """
        return self.__lines

    @property
    def descriptions(self) -> \
            typing.Generator[typing.Tuple[int, desc.Description], None, None]:
        """ an iterator for pairs of (line, description) """

        # A stack for repo folders
        path_stack = [self.__base_directory]

        for (i, l) in enumerate(self.lines):

            if isinstance(l, line.BaseLine):

                # extract the current and new order of the lines
                current_order = len(path_stack)
                new_order = l.depth

                # we can not have a new order lower than 1 depth of the
                # current level
                if new_order > current_order:
                    raise Exception(
                        'Error in line {}: Missing base sublevel. '.format(
                            i + 1))

                # Read the sub-directory to be added and the old one
                sub_dir = os.path.expanduser(l.path)
                previous_item = path_stack[new_order - 1]

                # add the new sub-directory
                new_sub_dir = os.path.join(previous_item, sub_dir)
                path_stack[new_order:] = [new_sub_dir]

                # and yield it
                yield i, desc.BaseDescription(new_sub_dir)

            if isinstance(l, line.RepoLine):
                # Extract the base directory and the source url
                stack_loc = path_stack[-1]
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

        for l in ll:
            if isinstance(l, line.RootLine):
                self.__root = os.path.join(self.__base_directory, l.root)
                break

        self.__lines = ll

    @property
    def root(self) -> str:
        """ The root of this repository"""

        return self.__root

    def index(self, d: desc.Description) -> typing.Optional[int]:
        """ Finds the index of a specific description inside of this Tree"""

        for (i, dd) in self.descriptions:
            if dd == d:
                return i

        return None

    def contains(self, d: desc.Description) -> bool:
        """ Checks if this repository contains a specific description """

        return self.index(d) is not None

    def insert_at(self, parent: typing.Optional[desc.BaseDescription],
                  d: desc.Description) -> int:
        """ Inserts a description at a given parent
        :param parent: Parent item to insert description at. If omitted,
        insert the item top-level
        :param d: Repository to insert
        """

        # are we inserting a base?
        insert_base = isinstance(d, desc.BaseDescription)

        # find the index to insert in
        # in the empty case, start at the top
        if parent is None:
            index = 0
            pdepth = 0

            indent = " "
        else:
            index = self.index(parent)
            if index is None:
                raise ValueError("Parent does not exist in Tree()")
            pdepth = self.lines[index].depth
            indent = self.lines[index].indent + " "
            index += 1

        # index to insert into
        insert_index = 0

        # A stack for repository patchs
        path_stack = [self.__base_directory]

        target_level = None

        # iterate through the lines
        # and find the last line
        for (i, l) in enumerate(self.lines):

            # only do thing for indexes below index
            if i >= index:

                # if we have a base line we might have to quit
                if isinstance(l, line.BaseLine):

                    # if we are not inserting a base, break
                    if not insert_base:
                        break

                    # if we do not know our target level yet, we need to
                    # find it
                    if target_level is None:
                        target_level = len(path_stack)

                    # we need to break upon our target level
                    if l.depth < target_level:
                        break

                # if we have a repo line and have not reached our target
                # level, we can save the indent
                if isinstance(l, line.RepoLine) and target_level is None:
                    indent = l.indent

            # else we might need to update our path
            elif isinstance(l, line.BaseLine):

                # extract the current and new order of the lines
                current_order = len(path_stack)
                new_order = l.depth

                # we can not have a new order lower than 1 depth of the
                # current level
                if new_order > current_order:
                    raise Exception(
                        'Error in line {}: Missing base sublevel. '.format(
                            i + 1))

                # Read the sub-directory to be added and the old one
                sub_dir = os.path.expanduser(l.path)
                previous_item = path_stack[new_order - 1]

                # add the new sub-directory
                new_sub_dir = os.path.join(previous_item, sub_dir)
                path_stack[new_order:] = [new_sub_dir]

            # and up the index to insert into
            insert_index = i + 1

        # the parent path is the path that is at the right most position
        ppath = path_stack[-1]

        # if we are inserting a repository, create an appropriate repo line
        if not insert_base:
            (base, item) = d.to_repo_line(indent, " ", "")
            if base.folder != ppath.rstrip("/"):
                raise ValueError("Cannot insert: Invalid Parent for "
                                 "RepositoryDescription. ")

        # if we are inserting a base description, we need to figure out paths
        else:
            npath = os.path.relpath(d.folder, ppath)
            if (npath == '..' or npath.startswith('../')):
                npath = d.folder
            item = line.BaseLine(indent, pdepth + 1, " ", npath, "")

        # finally insert the item itself
        self.__lines.insert(insert_index, item)

        # and return the inserted index
        return insert_index

    def insert_base_or_get(self, b: desc.BaseDescription) -> int:
        """ Gets a BaseDescription index or inserts it recursively """

        # if we have the parent already, we are done
        index = self.index(b)
        if index is not None:
            return index

        # if we are inside of the base path, we can go recursively
        if os.path.commonprefix([b.folder, self.__base_directory]) == \
                self.__base_directory:

            # find the parent base description
            (ppath, _) = os.path.split(b.folder)

            # if we have reached the base, we do not need to create anything
            if ppath != self.__base_directory \
                    and b.folder != self.__base_directory:
                parent = desc.BaseDescription(ppath)

                # and create the parent
                self.insert_base_or_get(parent)

            else:
                parent = None

        # else, we need to insert top-level
        else:
            parent = None

        # and finally create our base
        return self.insert_at(parent, b)

    def insert_repo_or_get(self, r: desc.RepositoryDescription) -> int:
        """ Gets a RepositoryDescription index or inserts it recursively """

        # inserting an already existing repo
        index = self.index(r)
        if index is not None:
            return index

        # else, we need to create the parent
        # unless it is the base
        (parent, _) = r.to_repo_line("", "", "")

        if parent.folder == self.__base_directory:
            parent = None
        else:
            self.insert_base_or_get(parent)

        # and then insert it
        return self.insert_at(parent, r)

    def rebuild(self):
        """ Rebuilds this configuration file by re-inserting all
        repository descriptions from scratch """

        # get all the repository descriptions
        repos = list(self.repositories)

        # wipe all the lines
        self.lines = []

        # if the root is not the base directory, insert it.
        if self.root != self.__base_directory:
            relroot = os.path.relpath(self.root, self.__base_directory)
            if relroot.startswith('..'):
                relroot = self.root

            self.lines.append(line.RootLine('', '', relroot, ''))

        # and re-insert all of the repos
        for r in repos:
            self.insert_repo_or_get(r)

    def remove_local(self, local: impl.LocalRepository) -> bool:
        """ Remove a local repository from a configuration file
        provided it exists """

        index = None

        # search for the local repository
        for (i, dd) in self.descriptions:
            if isinstance(dd, desc.RepositoryDescription) and \
              dd.local == local:
                index = i
                break

        # if we did not find it, return
        if index is None:
            return False

        # and remove the given index
        lines = self.lines
        del self.lines[index]
        self.lines = lines

        return True

    def find(self, pattern) -> typing.Generator[desc.Description, None, None]:
        """ Finds all repositories subject to a given description. """
        for r in self.repositories:
            if r.remote.matches(pattern):
                yield r
