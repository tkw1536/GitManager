import unittest
import unittest.mock

from GitManager.commands import state
from GitManager.repo import description
from GitManager.utils import format
from GitManager.repo import implementation


class TestState(unittest.TestCase):
    """ Tests that the fetch command works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository')
    @unittest.mock.patch(
        'builtins.print')
    def test_run(self,
                 builtins_print: unittest.mock.Mock,
                 implementation_LocalRepository: unittest.mock.Mock):
        # create a repository
        repo = description.RepositoryDescription('/path/to/source',
                                                 '/path/to/clone')

        # create a line
        line = format.TerminalLine()

        # and a command instance
        cmd = state.State(line, [repo], "--no-update")

        # if we are up-to-date, nothing should have been printed
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remote_status \
            .return_value = implementation.RemoteStatus.UP_TO_DATE
        self.assertTrue(cmd.run(repo))
        implementation_LocalRepository.return_value.remote_status \
            .assert_called_with(False)
        builtins_print.assert_not_called()

        # reset the mock
        implementation_LocalRepository.reset_mock()
        builtins_print.reset_mock()

        # create another command instance
        cmd = state.State(line, [repo], "--update")

        # if the local repository does not exist, we
        implementation_LocalRepository.return_value.exists.return_value = False
        self.assertFalse(cmd.run(repo))

        # reset the mock
        implementation_LocalRepository.reset_mock()
        builtins_print.reset_mock()

        # if we are up-to-date, nothing should have been printed
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remote_status \
            .return_value = implementation.RemoteStatus.UP_TO_DATE
        self.assertTrue(cmd.run(repo))
        implementation_LocalRepository.return_value.remote_status\
            .assert_called_with(True)
        builtins_print.assert_not_called()

        # reset the mock
        implementation_LocalRepository.reset_mock()
        builtins_print.reset_mock()

        # we need to pull
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remote_status \
            .return_value = implementation.RemoteStatus.REMOTE_NEWER
        self.assertFalse(cmd.run(repo))
        implementation_LocalRepository.return_value.remote_status \
            .assert_called_with(True)
        builtins_print.assert_called_with(
            format.Format.yellow('Upstream is ahead of your branch, '
                                 'pull required. '))

        # reset the mock
        implementation_LocalRepository.reset_mock()
        builtins_print.reset_mock()

        # we need to push
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remote_status \
            .return_value = implementation.RemoteStatus.LOCAL_NEWER
        self.assertFalse(cmd.run(repo))
        implementation_LocalRepository.return_value.remote_status \
            .assert_called_with(True)
        builtins_print.assert_called_with(
            format.Format.green('Your branch is ahead of upstream, '
                                'push required.'))

        # reset the mock
        implementation_LocalRepository.reset_mock()
        builtins_print.reset_mock()

        # divergence
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remote_status \
            .return_value = implementation.RemoteStatus.DIVERGENCE
        self.assertFalse(cmd.run(repo))
        implementation_LocalRepository.return_value.remote_status \
            .assert_called_with(True)
        builtins_print.assert_called_with(
            format.Format.red('Your branch and upstream have diverged, '
                              'merge or rebase required. '))
