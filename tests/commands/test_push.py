import unittest
import unittest.mock

from GitManager.commands import push
from GitManager.repo import description
from GitManager.utils import format


class TestPush(unittest.TestCase):
    """ Tests that the push command works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository')
    def test_run(self,
                 implementation_LocalRepository: unittest.mock.Mock):
        # create a repository
        repo = description.RepositoryDescription('/path/to/source',
                                                 '/path/to/clone')

        # create a command instance
        line = format.TerminalLine()
        cmd = push.Push(line, [repo])

        # if the local repository does not exist, we
        implementation_LocalRepository.return_value.exists.return_value = False
        self.assertFalse(cmd.run(repo))

        # reset the mock
        implementation_LocalRepository.reset_mock()

        # if the local repository does exist, it should have been pushed
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.push.return_value = True
        self.assertTrue(cmd.run(repo))
        implementation_LocalRepository.return_value.push.assert_called_with()
