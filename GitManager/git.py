import subprocess
import os.path

import sys

from . import run


class Git(object):
    """ Represents an interface to the git VCS"""

    @staticmethod
    def tuple_to_path(src, cwd, name=None):
        """
        Turns a tuple of (src, cwd, name) into a path to a clone.

        :param src: Source URI of the repository
        :type src: str

        :param cwd: Working directory of the Version Control System.
        :type cwd: str

        :param name: Name of the folder to clone VCS to.
        :type name: str

        :return: the path of the repository in absolute form.
        :rtype: str
        """

        # if the name is None, extract it from the URI
        if name is None:
            name = Git.get_humanish_part(src)

        # make the path
        path = os.path.join(cwd, name)

        # expand and return
        return os.path.expanduser(path)

    @staticmethod
    def get_humanish_part(uri):
        """
        Extracts the 'humanish' part of a URI. See the `man git-clone` for more
        details.

        :param uri: URI to extract humanish part from.
        :type uri: str

        :returns: A name representing the humanish part of the URI.
        :rtype: str
        """

        # Trim a trailing '.git'
        if uri.endswith('.git'):
            human = uri[:-4]
        else:
            human = uri

        # Trim trailing '/'s
        while human.endswith('/'):
            human = human[:-1]

        # And take the last part of the path.
        if '/' in human:
            human = human.split('/')[-1]

        # and return
        return human

    @staticmethod
    def exist_local(folder):
        """
        Checks if a local repository exists in the given folder. The folder may
        or may not exist.

        :param folder: Folder to check.
        :type folder: str

        :rtype: bool
        """

        # Check if it is a folder.
        if not os.path.isdir(folder):
            return False

        return run.GitRun("rev-parse", cwd=folder).success

    @staticmethod
    def clone(src, cwd, name=None):
        """ Clones a repository from the given source.

        :param src: Source URL to clone repo from.
        :type src: str

        :param cwd: Working directory to clone the repository from.
        :type cwd: str

        :param name: Name of folder to clone repository into. Must be relative
        to cwd. If omitted, extracts it automatically (see get_humanish_part).
        :type name: str

        :return: An indicator if the repository was successfully cloned.
        :rtype: bool
        """

        # ensure we have a name. If omitted, extract the 'humanish' part
        if name is None:
            name = Git.get_humanish_part(src)

        # find the full folder to clone to.
        full_path = os.path.join(cwd, name)

        # Create the cwd if it does not exist
        if not os.path.isdir(full_path):
            os.makedirs(full_path)

        return run.GitRun("clone", src, full_path, cwd=cwd).success

    @staticmethod
    def pull(path):
        """ Pulls (= updates) a git repository at the given path.

        :param path: Path to update repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        updated.
        :rtype: bool
        """
        # Temporary write a new line
        sys.stdout.write('\n')

        # run stuff
        r = run.GitRun("pull", cwd=path).success

        # And delete the new line again
        sys.stdout.write('\x1b[1A\x1b[2K\x1b[1A')

        return r

    @staticmethod
    def push(path):
        """ Pushes a git repository at the given path.

        :param path: Path to push repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        pushed.
        :rtype: bool
        """

        return run.GitRun("push", cwd=path).success

    @staticmethod
    def get_source(folder):
        """ Gets the source of the repository in the given folder

        :param folder: Folder to check in.
        :type folder: str

        :rtype: str
        """

        r = run.GitRun("remote", "get-url", "origin", cwd=folder)
        r.wait()

        return r.stdout.read().decode("utf-8")


__all__ = ["Git"]
