import unittest
import unittest.mock

from GitManager.commands import setup as s
from GitManager.repo import description
from GitManager.utils import format


class TestFetch(unittest.TestCase):
    """ Tests that the fetch command works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository')
    @unittest.mock.patch(
        'GitManager.repo.implementation.RemoteRepository')
    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    def test_run(self,
                 format_TerminalLine: unittest.mock.Mock,
                 implementation_RemoteRepository: unittest.mock.Mock,
                 implementation_LocalRepository: unittest.mock.Mock):
        # create a repository
        repo = description.RepositoryDescription('/path/to/source',
                                                 '/path/to/clone')

        # create a command instance
        line = format.TerminalLine()
        cmd = s.Setup(line, [repo])

        # if we already exist, nothing should happen
        implementation_LocalRepository.return_value.exists.return_value = True
        self.assertTrue(cmd.run(repo))
        implementation_RemoteRepository.return_value.clone.assert_not_called()

        # reset the mock
        format_TerminalLine.reset_mock()
        implementation_LocalRepository.reset_mock()
        implementation_RemoteRepository.reset_mock()

        # if the local repository does not exist, it should be cloned
        implementation_LocalRepository.return_value.exists.return_value = False
        implementation_RemoteRepository.return_value.clone.return_value = True
        self.assertTrue(cmd.run(repo))
        format_TerminalLine.return_value.linebreak.assert_called_with()
        implementation_RemoteRepository.return_value.clone \
            .assert_called_with(repo.local)
