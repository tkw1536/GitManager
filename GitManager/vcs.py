import subprocess
import os.path


class VCS(object):
    """ A class representing a version control system. """

    @classmethod
    def tuple_to_path(cls, src, cwd, name = None):
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
            name = cls.get_humanish_part(src)

        # make the path
        path = os.path.join(cwd, name)

        # expand and return
        return os.path.expanduser(path)

    @staticmethod
    def get_humanish_part(uri):
        """
        Extracts the 'humanish' part of a URI.

        :param uri: URI to extract humanish part from.
        :type uri: str

        :returns: A name representing the humanish part of the URI.
        :rtype: str
        """

        raise NotImplementedError

    @staticmethod
    def exist_local(folder):
        """
        Checks if a local repository exists in the given folder. The folder may
        or may not exist.

        :param folder: Folder to check.
        :type folder: str

        :rtype: bool
        """

        raise NotImplementedError

    @staticmethod
    def clone(src, cwd, name=None):
        """ Clones or checksout a repository from the given source.

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

        raise NotImplementedError

    @staticmethod
    def pull(path):
        """ Pulls (= updates) a repository at the given path.

        :param path: Path to update repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        updated.
        :rtype: bool
        """

        raise NotImplementedError

    @staticmethod
    def push(path):
        """ Pushes a repository at the given path.

        :param path: Path to push repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        pushed.
        :rtype: bool
        """

        raise NotImplementedError

    @staticmethod
    def get_source(folder):
        """ Gets the source of the repository in the given folder

        :param folder: Folder to check in.
        :type folder: str

        :rtype: str
        """

        raise NotImplementedError



class Git(VCS):
    """ Represents an interface to the git VCS"""

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

        # make two pipes to silence everything
        pipeA = open(os.devnull, 'wb')
        pipeB = open(os.devnull, 'wb')

        # and check if it exists there
        return subprocess.call(["git", "rev-parse"], stdout=pipeA, stderr=pipeB,
                               cwd=folder) == 0

    @staticmethod
    def clone(src, cwd, name = None):
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
        if not os.path.isdir(cwd):
            os.makedirs(cwd)

        return subprocess.call(["git", "clone", src, full_path], cwd=cwd) == 0

    @staticmethod
    def pull(path):
        """ Pulls (= updates) a git repository at the given path.

        :param path: Path to update repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        updated.
        :rtype: bool
        """

        return subprocess.call(["git", "pull"], cwd=path) == 0

    @staticmethod
    def push(path):
        """ Pushes a git repository at the given path.

        :param path: Path to push repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        pushed.
        :rtype: bool
        """

        return subprocess.call(["git", "push"], cwd=path) == 0

    @staticmethod
    def get_source(folder):
        """ Gets the source of the repository in the given folder

        :param folder: Folder to check in.
        :type folder: str

        :rtype: str
        """

        p = subprocess.call(["git", "remote", "get-url", "origin"], cwd=folder, stdout=subprocess.PIPE)
        p.communicate()

class Subversion(VCS):
    """ An interface to the subversion VCS. """

    @staticmethod
    def get_humanish_part(uri):
        """
        Extracts the 'humanish' part of a URI. See the `svn checkout --help` for more
        details.

        :param uri: URI to extract humanish part from.
        :type uri: str

        :returns: A name representing the humanish part of the URI.
        :rtype: str
        """

        human = uri

        # remove trailing /s
        while human.endswith('/'):
            human = human[:-1]

        # and get the basename
        return os.path.basename(human)

    @staticmethod
    def exist_local(folder):
        """
        Checks if a local repository exists in the given folder. The folder may
        or may not exist.

        :param folder: Folder to check.
        :type folder: str

        :rtype: bool
        """

        raise NotImplementedError

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

        return subprocess.call(["svn", "checkout", src, full_path], cwd=cwd) == 0

    @staticmethod
    def pull(path):
        """ Pulls (= updates) a subversion repository at the given path.

        :param path: Path to update repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        updated.
        :rtype: bool
        """

        return subprocess.call(["git", "up"], cwd=path) == 0

    @staticmethod
    def push(path):
        """ Unused method for subversion.

        :param path: Path to push repository at.
        :type path: str

        :return: An indicator indicating if the repository was successfully
        pushed.
        :rtype: bool
        """

        print("Will not auto-commit subversion repository, use svn commit manually. ")
        return False

__all__ = ["VCS", "Git", "Subversion"]