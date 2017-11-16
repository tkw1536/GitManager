import os
import re
import enum
import typing

import fnmatch

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

        self.__path = os.path.normpath(path)

    def __eq__(self, other: typing.Any) -> bool:
        """ Checks if this LocalRepository is equal to another"""
        return isinstance(other, LocalRepository) and other.path == self.path

    @property
    def remotes(self) -> typing.List[str]:
        """ A list of remotes that this RemoteRepository has """
        remotes = run.GitRun("remote", "show", "-n", cwd=self.path)
        remotes.wait()
        return remotes.stdout.read().decode("utf-8").split("\n")

    def get_remote_url(self, name: str) -> str:
        """ Get the url of a remote """

        # get the url of a remote
        remote_url = run.GitRun("remote", "get-url", name, cwd=self.path)

        # throw an exeception if we fail
        if not remote_url.success:
            raise ValueError("Unable to find remote {}".format(name))

        # else return the url
        return remote_url.stdout.read().decode("utf-8").split("\n")[0]

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

        # check if the directory exists
        if not os.path.isdir(self.path):
            return False

        # try to get the toplevel
        rev_parse_run = run.GitRun("rev-parse", "--show-toplevel",
                                   cwd=self.path)

        # if we did not succeed, we are not inside a git repo
        if not rev_parse_run.success:
            return False

        # get the actual toplevel
        toplevel = rev_parse_run.stdout.read().decode("utf-8").split("\n")[0]

        # and check that it is equal to the normal path
        return os.path.normpath(toplevel) == self.path

    def gc(self, *args: str) -> bool:
        """ Runs housekeeping tasks on this repository
        :param args: Arguments to pass along to the houskeeping command
        """

        return run.GitRun("gc", *args, cwd=self.path, pipe_stderr=True,
                          pipe_stdin=True, pipe_stdout=True).success

    def fetch(self) -> bool:
        """ Fetches all remotes from this repository"""

        return run.GitRun("fetch", "--all", "--quiet", cwd=self.path,
                          pipe_stdin=True, pipe_stdout=True,
                          pipe_stderr=True).success

    def pull(self) -> bool:
        """ Pulls all remotes from this repository"""

        return run.GitRun("pull", cwd=self.path, pipe_stdin=True,
                          pipe_stdout=True, pipe_stderr=True).success

    def push(self) -> bool:
        """ Pushes this repository """

        return run.GitRun("push", cwd=self.path, pipe_stdin=True,
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

    def remote_status(self, update=False) -> typing.Optional[RemoteStatus]:
        """ Shows status on this repository, and in particular if it i
        out-of-date with the remote

        :param update: Boolean indicating if we should update using git
        remote update first
        """

        # if we do not exist, return
        if not self.exists():
            return None

        # if we should update, run git remote update
        if update:
            if not run.GitRun("remote", "update", cwd=self.path).success:
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

    def clone(self, local: LocalRepository, *args: typing.Tuple[str]) -> bool:
        """ Clones this repository into the path given by a local path"""
        return run.GitRun("clone", self.url, local.path, *args,
                          pipe_stdin=True, pipe_stdout=True,
                          pipe_stderr=True).success

    def components(self) -> typing.List[str]:
        """
        Extracts the components of this URL, i.e. a set of items that uniquely
        identifies where this repository should go.
        """

        # Trim a trailing '.git'
        if self.url.endswith('.git'):
            url = self.url[:-4]
        else:
            url = self.url

        # Trim trailing '/'s
        while url.endswith('/'):
            url = url[:-1]

        if '://' in url:
            # [$PROTOCOL]:$PREFIX/$COMPONENTS
            url = '://'.join(url.split('://')[1:])
            parts = re.split(r"[\\/:]", url)
            (prefix, rest) = (parts[0], '/'.join(parts[1:]))
        else:
            # $PREFIX:$COMPONENTS
            parts = url.split(':')
            (prefix, rest) = (parts[0], ':'.join(parts[1:]))

        # read (user, host) from the prefix
        if '@' in prefix:
            parts = prefix.split('@')
            (user, host) = (parts[0], '@'.join(parts[1:]))
        else:
            user = None
            host = prefix

        # if user is 'git' or 'gogs', ignore it
        if user in ['git', 'gogs']:
            user = None

        # prepare to prepend prefix
        if user is not None:
            prefix = [host, user]
        else:
            prefix = [host]

        # and split into '/'s
        return prefix + re.split(r"[\\/:]", rest)

    def matches(self, pattern: str) -> bool:
        """ Checks if a repository matches a given pattern"""

        # lowercase the pattern
        pattern = pattern.lower()

        # split the pattern into components
        if ':' in pattern:
            pattern_components = RemoteRepository(pattern).components()
        else:
            pattern = ':' + pattern
            pattern_components = RemoteRepository(pattern).components()[1:]

        # count and reassemble
        pattern_length = len(pattern_components)
        pattern = '/'.join(pattern_components)

        # get the components of the current repo
        components = list(map(lambda pc: pc.lower(), self.components()))
        components_length = len(components)

        # iterate over all sub-paths of the given length
        for i in range(components_length - pattern_length + 1):
            suburl = '/'.join(components[i:i + pattern_length])
            if fnmatch.fnmatch(suburl, pattern):
                return True

        return False

    def humanish_part(self) -> str:
        """
        Extracts the 'humanish' part of this URL. See the `man git-clone`
        for more details.
        """

        return self.components()[-1]
