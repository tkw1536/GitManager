import unittest
import unittest.mock

from GitManager.commands import status
from GitManager.repo import description
from GitManager.utils import format


class TestStatus(unittest.TestCase):
    """ Tests that the status command works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository')
    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_run(self,
                 run_gitrun: unittest.mock.Mock,
                 format_TerminalLine: unittest.mock.Mock,
                 implementation_LocalRepository: unittest.mock.Mock):
        # create a repository
        repo = description.RepositoryDescription('/path/to/source',
                                                 '/path/to/clone')

        # create a command instance
        line = format.TerminalLine()
        cmd = status.Status(line, [repo])

        # if the local repository does not exist, do nothing
        implementation_LocalRepository.return_value.exists.return_value = False
        implementation_LocalRepository.return_value.path.return_value = \
            '/path/to/clone'
        self.assertFalse(cmd.run(repo))
        implementation_LocalRepository.exists.assert_not_called()

        # reset the mock
        format_TerminalLine.reset_mock()
        implementation_LocalRepository.reset_mock()
        run_gitrun.reset_mock()

        # local repository exists, but is clean
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.path.return_value = \
            '/path/to/clone'
        implementation_LocalRepository.return_value.local_status.return_value \
            = ''
        self.assertTrue(cmd.run(repo))
        run_gitrun.assert_not_called()

        # reset the mock
        format_TerminalLine.reset_mock()
        implementation_LocalRepository.reset_mock()
        run_gitrun.reset_mock()

        # local repository exists, but is not clean
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.path = \
            '/path/to/clone'
        implementation_LocalRepository.return_value.local_status.return_value \
            = 'M some/file'
        self.assertFalse(cmd.run(repo))
        format_TerminalLine.return_value.linebreak.assert_called_with()
        run_gitrun.assert_called_with('status', cwd='/path/to/clone',
                                      pipe_stdout=True)
        run_gitrun.return_value.wait.assert_called_with()
