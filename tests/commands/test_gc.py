import unittest
import unittest.mock

from GitManager.commands import gc
from GitManager.repo import description
from GitManager.utils import format


class TestGC(unittest.TestCase):
    """ Tests that the fetch command works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository')
    def test_run(self,
                 implementation_LocalRepository: unittest.mock.Mock):
        # create a repository
        repo = description.RepositoryDescription('/path/to/source',
                                                 '/path/to/clone')

        # create a command instance
        line = format.TerminalLine()
        cmd = gc.GC(line, [repo])

        # if the local repository does not exist, we do nothing
        implementation_LocalRepository.return_value.exists.return_value = False
        self.assertFalse(cmd.run(repo))
        implementation_LocalRepository.return_value.gc.assert_not_called()

        # reset the mock
        implementation_LocalRepository.reset_mock()

        # if the local repository does exist, it should have been gced
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.gc.return_value = True
        self.assertTrue(cmd.run(repo))
        implementation_LocalRepository.return_value.gc.assert_called_with()

        # reset the mock and create a new mock
        implementation_LocalRepository.reset_mock()

        cmd = gc.GC(line, [repo], '--aggressive')
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.gc.return_value = True
        self.assertTrue(cmd.run(repo))
        implementation_LocalRepository.return_value.gc.assert_called_with(
            '--aggressive')
