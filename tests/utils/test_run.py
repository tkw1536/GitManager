import unittest
import unittest.mock

import subprocess

from GitManager.utils import run


class TestRun(unittest.TestCase):
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_init(self, os_environ_copy: unittest.mock.Mock,
                  os_getcwd_mock: unittest.mock.Mock):
        """ Tests that run instances are created properly """

        # almost everything is default
        run1 = run.ProcessRun("echo", "Hello world")

        os_environ_copy.assert_called_once_with()
        os_getcwd_mock.assert_called_once_with()
        self.assertEqual(run1.exe, 'echo')
        self.assertEqual(run1.args, ['Hello world'])
        self.assertEqual(run1.cwd, '/')
        self.assertEqual(run1.environment, {})
        self.assertEqual(run1.pipe_stdout, False)
        self.assertEqual(run1.pipe_stderr, False)
        self.assertEqual(run1.pipe_stdin, False)

        # and reset the mocks please
        os_environ_copy.reset_mock()
        os_getcwd_mock.reset_mock()

        # use some non-default values
        run2 = run.ProcessRun("echo", "Hello world", cwd='/hello',
                              pipe_stdout=True, environment={'hello': 'world'})
        os_environ_copy.assert_not_called()
        os_getcwd_mock.assert_not_called()
        self.assertEqual(run2.exe, 'echo')
        self.assertEqual(run2.args, ['Hello world'])
        self.assertEqual(run2.cwd, '/hello')
        self.assertEqual(run2.environment, {'hello': 'world'})
        self.assertEqual(run2.pipe_stdout, True)
        self.assertEqual(run2.pipe_stderr, False)
        self.assertEqual(run2.pipe_stdin, False)

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_stdout(self, os_environ_copy: unittest.mock.Mock,
                    os_getcwd_mock: unittest.mock.Mock,
                    subprocess_popen: unittest.mock.Mock):
        """ Tests that stdout works properly"""

        # fake the return value of stdout
        subprocess_popen.return_value.stdout = ''

        # create a run where we do not pipe stdout
        run1 = run.ProcessRun("echo", pipe_stdout=False)

        # in the ready state we should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run1.stdout

        # once we run, we should return the normal value
        run1.run()
        self.assertEqual(run1.stdout, '')

        # create a run where we do pipe stdout
        run2 = run.ProcessRun("echo", pipe_stdout=True)

        # in the ready state we should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run2.stdout

        # once we run, we should return None (because piping)
        run2.run()
        self.assertEqual(run2.stdout, None)

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_stderr(self, os_environ_copy: unittest.mock.Mock,
                    os_getcwd_mock: unittest.mock.Mock,
                    subprocess_popen: unittest.mock.Mock):
        """ Tests that stderr works properly"""

        # fake the return value of stderr
        subprocess_popen.return_value.stderr = ''

        # create a run where we do not pipe stderr
        run1 = run.ProcessRun("echo", pipe_stderr=False)

        # in the ready state we should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run1.stderr

        # once we run, we should return the normal value
        run1.run()
        self.assertEqual(run1.stderr, '')

        # create a run where we do pipe stderr
        run2 = run.ProcessRun("echo", pipe_stderr=True)

        # in the ready state we should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run2.stderr

        # once we run, we should return None (because piping)
        run2.run()
        self.assertEqual(run2.stderr, None)

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_stdin(self, os_environ_copy: unittest.mock.Mock,
                   os_getcwd_mock: unittest.mock.Mock,
                   subprocess_popen: unittest.mock.Mock):
        """ Tests that stdin works properly"""

        # fake the return value of stdin
        subprocess_popen.return_value.stdin = ''

        # create a run where we do not pipe stdin
        run1 = run.ProcessRun("echo", pipe_stdin=False)

        # in the ready state we should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run1.stdin

        # once we run, we should return the normal value
        run1.run()
        self.assertEqual(run1.stdin, '')

        # create a run where we do pipe stdin
        run2 = run.ProcessRun("echo", pipe_stdin=True)

        # in the ready state we should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run2.stdin

        # once we run, we should return None (because piping)
        run2.run()
        self.assertEqual(run2.stdin, None)

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_state(self, os_environ_copy: unittest.mock.Mock,
                   os_getcwd_mock: unittest.mock.Mock,
                   subprocess_popen: unittest.mock.Mock):
        """ Tests that state calls work properly """

        # create a new run instance
        run1 = run.ProcessRun("echo")

        # should start out with the ready() state
        self.assertEqual(run1.state, run.ProcessRunState.NEW)

        # we now run it and return None
        run1.run()
        subprocess_popen.return_value.returncode = None

        # which means we are always alive
        self.assertEqual(run1.state, run.ProcessRunState.ACTIVE)

        # once we have a return code we are finished
        subprocess_popen.return_value.returncode = 0
        self.assertEqual(run1.state, run.ProcessRunState.TERMINATED)

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_run(self, os_environ_copy: unittest.mock.Mock,
                 os_getcwd_mock: unittest.mock.Mock,
                 subprocess_popen: unittest.mock.Mock):
        """ tests that run() calls work properly """

        # make a (fairly default) run
        run1 = run.ProcessRun("echo")

        # run the process -- it should make a call to subprocess.Popen
        run1.run()
        subprocess_popen.assert_called_with(['echo'], cwd='/',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE, env={})

        # and if you try to run it again, it should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run1.run()

        # reset the mock
        subprocess_popen.reset_mock()

        # make a (non-default) run
        run2 = run.ProcessRun("echo", "Hello world", pipe_stdout=True,
                              pipe_stderr=True, pipe_stdin=True,
                              cwd='/hello', environment={'hello': 'world'})

        # run the process -- it should make a call to subprocess.Popen
        run2.run()
        subprocess_popen.assert_called_with(['echo', 'Hello world'],
                                            cwd='/hello',
                                            stdout=None,
                                            stderr=None,
                                            stdin=None, env={'hello': 'world'})

        # and if you try to run it again, it should raise an error
        with self.assertRaises(run.ProcessRunStateError):
            run2.run()

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_wait(self, os_environ_copy: unittest.mock.Mock,
                  os_getcwd_mock: unittest.mock.Mock,
                  subprocess_popen: unittest.mock.Mock):
        """ Makes sure that the wait call works properly"""

        # make a new run and wait for the default amount of time
        run1 = run.ProcessRun("echo")
        run1.wait()

        # wait() should have been called with None
        subprocess_popen.assert_called_with(['echo'], cwd='/',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE, env={})
        subprocess_popen.return_value.wait.assert_called_with(timeout=None)
        subprocess_popen.reset_mock()

        # make a new run and wait for a fixed amount of time
        run2 = run.ProcessRun("echo")
        run2.wait(100)

        # wait should have been called with Some()
        subprocess_popen.assert_called_with(['echo'], cwd='/',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE, env={})
        subprocess_popen.return_value.wait.assert_called_with(timeout=100)

        # this time run manually and pretend it is rzunning
        run3 = run.ProcessRun("echo")
        run3.run()
        subprocess_popen.return_value.returncode = None

        # reset all the call counters
        subprocess_popen.reset_mock()

        # and now we should wait for 100
        run3.wait(100)
        subprocess_popen.assert_not_called()
        subprocess_popen.return_value.wait.assert_called_with(timeout=100)

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_kill(self, os_environ_copy: unittest.mock.Mock,
                  os_getcwd_mock: unittest.mock.Mock,
                  subprocess_popen: unittest.mock.Mock):
        """ tests that killing works properly"""

        # make a new run and wait for the default amount of time
        run1 = run.ProcessRun("echo")

        # we can not kill it if it is not running.
        with self.assertRaises(run.ProcessRunStateError):
            run1.kill()

        # run the process and properly pretend that it is alive
        run1.run()
        subprocess_popen.return_value.returncode = None

        # now we can kill
        run1.kill()
        subprocess_popen.return_value.kill.assert_called_with()

        # pretend we have finished
        subprocess_popen.return_value.returncode = 1

        # we should not be able to kill anymore
        with self.assertRaises(run.ProcessRunStateError):
            run1.kill()

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_returncode(self, os_environ_copy: unittest.mock.Mock,
                        os_getcwd_mock: unittest.mock.Mock,
                        subprocess_popen: unittest.mock.Mock):
        """ Tests that the returncode attribute works properly """

        # make a new run and wait for the default amount of time
        run1 = run.ProcessRun("echo")

        # mock the returncode of the call
        subprocess_popen.return_value.returncode = 0
        self.assertEqual(run1.returncode, 0)

        # we should have called the subprocess
        subprocess_popen.assert_called_with(['echo'], cwd='/',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE, env={})
        # and a wait call
        subprocess_popen.return_value.wait.assert_called_with(timeout=None)

        # make another call
        run2 = run.ProcessRun("echo")
        run2.run()
        subprocess_popen.return_value.returncode = 1

        subprocess_popen.reset_mock()

        self.assertEqual(run2.returncode, 1)
        subprocess_popen.assert_not_called()
        subprocess_popen.return_value.wait.assert_not_called()

    @unittest.mock.patch('subprocess.Popen')
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_success(self, os_environ_copy: unittest.mock.Mock,
                     os_getcwd_mock: unittest.mock.Mock,
                     subprocess_popen: unittest.mock.Mock):
        """ Tests that the success attribute works properly """

        # make a new run and wait for the default amount of time
        run1 = run.ProcessRun("echo")

        # mock the returncode of the call
        subprocess_popen.return_value.returncode = 0
        self.assertEqual(run1.success, True)

        # we should have called the subprocess
        subprocess_popen.assert_called_with(['echo'], cwd='/',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdin=subprocess.PIPE, env={})
        # and a wait call
        subprocess_popen.return_value.wait.assert_called_with(timeout=None)

        # make another call
        run2 = run.ProcessRun("echo")
        run2.run()
        subprocess_popen.return_value.returncode = 1

        subprocess_popen.reset_mock()

        self.assertEqual(run2.success, False)
        subprocess_popen.assert_not_called()
        subprocess_popen.return_value.wait.assert_not_called()


class TestGitRun(unittest.TestCase):
    @unittest.mock.patch('os.getcwd', return_value='/')
    @unittest.mock.patch('os.environ.copy', return_value={})
    def test_init(self, os_environ_copy: unittest.mock.Mock,
                  os_getcwd_mock: unittest.mock.Mock):
        """ Tests that GitRun instances are created properly """

        # almost everything is default
        run1 = run.GitRun("Hello world")

        os_environ_copy.assert_called_once_with()
        os_getcwd_mock.assert_called_once_with()
        self.assertEqual(run1.exe, 'git')
        self.assertEqual(run1.args, ['Hello world'])
        self.assertEqual(run1.cwd, '/')
        self.assertEqual(run1.environment, {})
        self.assertEqual(run1.pipe_stdout, False)
        self.assertEqual(run1.pipe_stderr, False)
        self.assertEqual(run1.pipe_stdin, False)

        # and reset the mocks please
        os_environ_copy.reset_mock()
        os_getcwd_mock.reset_mock()

        # use some non-default values
        run2 = run.GitRun("Hello world", cwd='/hello',
                          pipe_stdout=True, environment={'hello': 'world'})
        os_environ_copy.assert_not_called()
        os_getcwd_mock.assert_not_called()
        self.assertEqual(run2.exe, 'git')
        self.assertEqual(run2.args, ['Hello world'])
        self.assertEqual(run2.cwd, '/hello')
        self.assertEqual(run2.environment, {'hello': 'world'})
        self.assertEqual(run2.pipe_stdout, True)
        self.assertEqual(run2.pipe_stderr, False)
        self.assertEqual(run2.pipe_stdin, False)
