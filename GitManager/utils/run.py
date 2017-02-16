import typing
import enum
import subprocess
import os


class ProcessRunState(enum.Enum):
    """ Different process run states """

    NEW = 'new'
    ACTIVE = 'active'
    TERMINATED = 'terminated'


class ProcessRun(object):
    """ Represents a single call to an external Executable """

    def __init__(self, exe: str, *args: typing.List[str],
                 cwd: typing.Optional[str] = None, pipe_stdout: bool = False,
                 pipe_stderr: bool = False, pipe_stdin: bool = False,
                 environment: typing.Optional[dict] = None):
        """
        :param exe: Executable or command to run
        :param args: Arguments to the git call
        :param cwd: Working directory of the git call. Defaults to the
        current working directory
        :param pipe_stdout: should we pipe stdout to the parent?
        :param pipe_stderr: should we pipe stderr to the parent?
        :param pipe_stdin: should we pipe stdin from the parent?

        :param environment: The environment of this process or None if it
        should be inherited from the parent
        """

        self.__exe = exe
        self.__args = list(args)
        self.__cwd = cwd if cwd is not None else os.getcwd()

        self.__pipe_stdout = pipe_stdout
        self.__pipe_stdin = pipe_stdin
        self.__pipe_stderr = pipe_stderr

        self.__environment = environment if environment is not None else \
            os.environ.copy()

        # Has the process been started?
        self.__started = False

        # The Popen handle of the process
        self.__handle = None  # type: subprocess.Popen

    #
    # PROPERTIES
    #

    @property
    def exe(self) -> str:
        """ Command (executable) to run in this process run """

        # TODO: Do we want to have a which() here?

        return self.__exe

    @property
    def args(self) -> typing.List[str]:
        """ arguments given to this Git command """
        return self.__args

    @property
    def cwd(self) -> str:
        """ working directory of the GitRun() """
        return self.__cwd

    @property
    def environment(self) -> dict:
        """ environment of this process """
        return self.__environment

    #
    # INPUT / OUTPUT
    #

    @property
    def pipe_stdout(self) -> bool:
        """ should we pipe stdout to the parent? """
        return self.__pipe_stdout

    @property
    def stdout(self) -> typing.Optional[typing.IO[bytes]]:
        """ the stdout handle of the process or None """

        # we need to run the process first
        if self.state == ProcessRunState.NEW:
            raise ProcessRunStateError('ProcessRun() is not running')

        # if we are not piping stdout to the parent, return it
        if not self.pipe_stdout:
            return self.__handle.stdout

        # else we return None
        else:
            return None

    @property
    def pipe_stderr(self) -> bool:
        """ should we pipe stderr to the parent? """
        return self.__pipe_stderr

    @property
    def stderr(self) -> typing.Optional[typing.IO[bytes]]:
        """ the stderr handle of the process or None """

        # we need to run the process first
        if self.state == ProcessRunState.NEW:
            raise ProcessRunStateError('ProcessRun() is not running')

        # if we are piping stdout, we return it
        if not self.pipe_stderr:
            return self.__handle.stderr

        # else we return None
        else:
            return None

    @property
    def pipe_stdin(self) -> bool:
        """ should we pipe stdin to the parent? """
        return self.__pipe_stdin

    @property
    def stdin(self) -> typing.Optional[typing.IO[bytes]]:
        """ the stdin handle of the process or None """

        # we need to run the process first
        if self.state == ProcessRunState.NEW:
            raise ProcessRunStateError('ProcessRun() is not running')

        # if we are piping stdout, we return it
        if not self.pipe_stdin:
            return self.__handle.stdin

        # else we return None
        else:
            return None

    @property
    def returncode(self) -> int:
        """ the returncode of this process (blocking) """

        # if we we are not yet finished, wait
        if self.state != ProcessRunState.TERMINATED:
            self.wait()

        return self.__handle.returncode

    @property
    def success(self) -> bool:
        """ success of this process, i.e. if its returncode was 0 """
        return self.returncode == 0

    #
    # STATE
    #

    @property
    def state(self) -> ProcessRunState:
        """
        The current state of the process -- has it been started, finished,
        etc.
        :return: one of 'ready', 'running', 'finished'
        """

        # we have not been started yet
        if not self.__started:
            return ProcessRunState.NEW

        # Poll to check if we have finished
        self.__handle.poll()

        # still running
        if self.__handle.returncode is None:
            return ProcessRunState.ACTIVE

        # else return finished
        else:
            return ProcessRunState.TERMINATED

    def run(self):
        """ Runs this process """

        # check that we have not yet been started
        if self.state != ProcessRunState.NEW:
            raise ProcessRunStateError(
                'ProcessRun() was already started, can not run it again. ')

        # Set the output arguments correctly
        stdout = None if self.pipe_stdout else subprocess.PIPE
        stderr = None if self.pipe_stderr else subprocess.PIPE
        stdin = None if self.pipe_stdin else subprocess.PIPE

        # We are now running
        self.__started = True

        # Make the arguments ready
        self.__handle = subprocess.Popen([self.exe] + self.args, cwd=self.cwd,
                                         stdout=stdout, stderr=stderr,
                                         stdin=stdin, env=self.environment)

    def wait(self, timeout: typing.Optional[int] = None):
        """ waits for this process to finish
        :param timeout: Optional timeout to wait for
        """

        # we are not yet running, so start it
        if self.state == ProcessRunState.NEW:
            self.run()

        # and wait for the process
        self.__handle.wait(timeout=timeout)

    def kill(self):
        """ kills this process """

        # we can only kill a running process
        if self.state != ProcessRunState.ACTIVE:
            raise ProcessRunStateError('can only kill running process')

        self.__handle.kill()


class GitRun(ProcessRun):
    def __init__(self, *args: str,
                 cwd: typing.Optional[str] = None, pipe_stdout: bool = False,
                 pipe_stderr: bool = False, pipe_stdin: bool = False,
                 environment: typing.Optional[dict] = None):
        """
        :param args: Arguments to the git call
        :param cwd: Working directory of the git call. Defaults to the
        current working directory
        :param pipe_stdout: should we pipe stdout to the parent?
        :param pipe_stderr: should we pipe stderr to the parent?
        :param pipe_stdin: should we pipe stdin from the parent?

        :param environment: The environment of this process or None if it
        should be inherited from the parent
        """

        super().__init__("git", *args, cwd=cwd, pipe_stdout=pipe_stdout,
                         pipe_stderr=pipe_stderr, pipe_stdin=pipe_stdin,
                         environment=environment)


class ProcessRunStateError(Exception):
    """ An error in the state of the ProcessRun """
    pass
