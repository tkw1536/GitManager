import unittest
import unittest.mock

from GitManager.commands import lister
from GitManager.repo import description
from GitManager.utils import format


class TestFetch(unittest.TestCase):
    """ Tests that the lister command works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository')
    @unittest.mock.patch('builtins.print')
    def test_run(self,
                 builtins_print: unittest.mock.Mock,
                 implementation_LocalRepository: unittest.mock.Mock):
        # create a repository
        repo = description.RepositoryDescription('/path/to/source',
                                                 '/path/to/clone')

        # create a command instance
        line = format.TerminalLine()
        cmd = lister.LsLocal(line, [repo])

        # if the local repository does not exist, we just return false
        implementation_LocalRepository.return_value.exists.return_value = False
        self.assertTrue(cmd.run(repo))
        builtins_print.assert_not_called()

        # reset the mock
        builtins_print.reset_mock()
        implementation_LocalRepository.reset_mock()

        # if the local repository does exist, it should have been fetched
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.path = "/path/to/clone"
        self.assertTrue(cmd.run(repo))
        builtins_print.assert_called_with('/path/to/clone')
