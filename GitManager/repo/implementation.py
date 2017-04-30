import os
import enum
import typing

from ..utils import run


class RemoteStatus(enum.Enum):
    """ Remote uplink status"""
    UP_TO_DATE = "ok"
    REMOTE_NEWER = "pull"
    LOCAL_NEWER = "push"
    DIVERGENCE = "divergence"


class LocalRepository(object):
    """ Represents a local repository identified by a path """

    def __init__(self, path: str):
        """ Creates a new LocalRepository """

        self.__path = path

    def __eq__(self, other: typing.Any) -> bool:
        """ Checks if this LocalRepository is equal to another"""
        return isinstance(other, LocalRepository) and other.path == self.path

    @property
    def remotes(self) -> typing.List[str]:
        """ A list of remotes that this RemoteRepository has """
        remotes = run.GitRun("remote", "show", "-n", cwd=self.path)
        remotes.wait()
        return remotes.stdout.read().decode("utf-8").split("\n")

    @property
    def path(self) -> str:
        """ The path to this repository """
        return self.__path

    def upstream_ref(self, ref: str) -> str:
        """ Gets the upstream being tracked by a given path

        :param ref: Ref to get upstream of.
        """

        refs = run.GitRun("for-each-ref", "--format=%(upstream:short)", ref,
                          cwd=self.path)
        refs.wait()

        return refs.stdout.read().decode("utf-8").split("\n")[0]

    def symbolic_ref(self, ref: str) -> str:
        """ Gets the symbolic ref REF is pointing to

        :param ref: Ref to parse
        """

        refs = run.GitRun("symbolic-ref", "-q", ref, cwd=self.path)
        refs.wait()

        return refs.stdout.read().decode("utf-8").split("\n")[0]

    def ref_parse(self, ref: str) -> str:
        """ Normalises a ref by parsing it in a short form
        :param ref: Ref to parse
        """

        refs = run.GitRun("rev-parse", ref, cwd=self.path)
        refs.wait()

        return refs.stdout.read().decode("utf-8").split("\n")[0]

    def __str__(self) -> str:
        return self.path

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, str(self))

    def exists(self) -> bool:
        """ Checks if this repository exists """

        if not os.path.isdir(self.path):
            return False

        # TODO: Check that we are indeed in the toplevel
        return run.GitRun("rev-parse", cwd=self.path).success

    def fetch(self) -> bool:
        """ Fetches all remotes from this repository"""

        return run.GitRun("fetch", "--all", "--quiet", cwd=self.path,
                          pipe_stdin=True, pipe_stdout=True,
                          pipe_stderr=True).success

    def pull(self) -> bool:
        """ Pulls all remotes from this repository"""

        return run.GitRun("pull", cwd=self.path, pipe_stdin=True,
                          pipe_stdout=True, pipe_stderr=True).success

    def local_status(self) -> typing.Optional[str]:
        """ Shows status on this git repository
        """

        if not self.exists():
            return None

        # Check for the status first
        cmd = run.GitRun("status", "--porcelain", cwd=self.path)
        cmd.wait()

        # return the porcelain info
        return cmd.stdout.read().decode("utf-8")

    def remote_status(self) -> typing.Optional[RemoteStatus]:
        """ Shows status on this repository, and in particular if it i
        out-of-date with the remote
        """

        # if we do not exist, return
        if not self.exists():
            return None

        # where is head pointing to?
        localref = self.ref_parse("HEAD")

        # what is our upstream?
        upstream = self.upstream_ref(self.symbolic_ref("HEAD"))
        remoteref = self.ref_parse(upstream)

        # check where we would merge
        refs = run.GitRun("merge-base", localref, remoteref, cwd=self.path)
        refs.wait()
        baseref = refs.stdout.read().decode("utf-8").split("\n")[0]

        # if both references are identical, we are ok
        if localref == remoteref:
            return RemoteStatus.UP_TO_DATE

        # if we would start with the local base, we would have to pull
        elif localref == baseref:
            return RemoteStatus.REMOTE_NEWER

        # if we would start with the remote base, we would have to push
        elif remoteref == baseref:
            return RemoteStatus.LOCAL_NEWER

        # else we have divergence and something is wrong.
        else:
            return RemoteStatus.DIVERGENCE


class RemoteRepository(object):
    """ Represents a remote repository identified by a url """

    def __init__(self, url: str):
        """ creates a new RemoteRepository()

        :param url: URL to remote repository
        """
        self.__url = url

    def __eq__(self, other: typing.Any) -> bool:
        """ Checks if this LocalRepository is equal to another"""
        return isinstance(other, RemoteRepository) and other.url == self.url

    @property
    def url(self) -> str:
        """ the url to this repository """
        return self.__url

    def __str__(self) -> str:
        return self.url

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, str(self))

    def exists(self) -> bool:
        """ Checks if this remote repository exists """
        return run.GitRun("ls-remote", "--exit-code", self.url).success

    def clone(self, local: LocalRepository) -> bool:
        """ Clones this repository into the path given by a local path"""
        return run.GitRun("clone", self.url, local.path,
                          pipe_stdin=True, pipe_stdout=True,
                          pipe_stderr=True).success

    def humanish_part(self) -> str:
        """
        Extracts the 'humanish' part of this URL. See the `man git-clone`
        for more details.
        """

        # Trim a trailing '.git'
        if self.url.endswith('.git'):
            human = self.url[:-4]
        else:
            human = self.url

        # Trim trailing '/'s
        while human.endswith('/'):
            human = human[:-1]

        # And take the last part of the path.
        if '/' in human:
            human = human.split('/')[-1]

        # and return
        return human