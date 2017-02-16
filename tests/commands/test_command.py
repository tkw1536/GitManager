import unittest
import unittest.mock

from GitManager import commands
from GitManager.utils import format
from GitManager.repo import description


class TestCommand(unittest.TestCase):
    """ Tests that the command line works properly """

    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository.exists',
        side_effect=[True, False])
    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    def test_repos(self, format_TerminalLine: unittest.mock.Mock,
                   implementation_exists: unittest.mock.Mock):
        """ Tests that the list of repos works properly """

        line = format.TerminalLine()
        repos = [
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/other/source', '/path/to/other/clone')
        ]

        # create a command object
        cmd = commands.Command(line, repos)

        # if we have a local command, only show the existing one
        with unittest.mock.patch('GitManager.commands.Command.LOCAL',
                                 True):
            self.assertEqual(cmd.repos, repos[0:1])

        # if we do not have a local command, show all
        with unittest.mock.patch('GitManager.commands.Command.LOCAL',
                                 False):
            self.assertEqual(cmd.repos, repos)

    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    def test_run(self, format_TerminalLine: unittest.mock.Mock):
        """ Tests that the run() method is not implemented. """

        # create a magic line object
        line = format.TerminalLine()
        repos = []

        # create a command object
        cmd = commands.Command(line, repos)

        # and make sure it throws an error:
        with self.assertRaises(NotImplementedError):
            cmd.run(description.RepositoryDescription('/path/to/source',
                                                      '/path/to/clone'))

    @unittest.mock.patch('builtins.print')
    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    def test_write(self, format_TerminalLine: unittest.mock.Mock,
                   builtins_print: unittest.mock.Mock):
        """ Tests that the write function works properly. """

        line = format.TerminalLine()
        repos = []

        # create a command object
        cmd = commands.Command(line, repos)

        # write hello world
        cmd.write("Hello world")

        # assert that the right calls have been made
        format_TerminalLine.return_value.linebreak.assert_called_with()
        builtins_print.assert_called_with("Hello world")

    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    def test_write_with_counter(self,
                                format_TerminalLine: unittest.mock.Mock):
        """ Tests that the write_with_counter function works correctly"""

        format_TerminalLine.return_value.width = 100
        line = format.TerminalLine()

        repos = [
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone')
        ]

        # create a command object
        cmd = commands.Command(line, repos)
        cmd._Command__idx = 2

        cmd.write_with_counter('SOME TEXT')
        format_TerminalLine.return_value.write \
            .assert_called_with("[03/11] SOME TEXT")

    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    def test_write_path_with_counter(self,
                                     format_TerminalLine: unittest.mock.Mock):
        """ Tests that the write_with_counter function works correctly"""

        format_TerminalLine.return_value.width = 21
        line = format.TerminalLine()

        repos = [
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone')
        ]

        # create a command object
        cmd = commands.Command(line, repos)
        cmd._Command__idx = 2

        cmd.write_path_with_counter('/path/to/clone')
        format_TerminalLine.return_value.write \
            .assert_called_with("[03/11] /path/.../...")

    @unittest.mock.patch('GitManager.utils.format.TerminalLine')
    @unittest.mock.patch('GitManager.commands.Command.write_path_with_counter')
    @unittest.mock.patch('GitManager.commands.Command.run', return_value=True)
    def test_call(self,
                  command_run: unittest.mock.Mock,
                  command_write_path_with_counter: unittest.mock.Mock,
                  format_TerminalLine: unittest.mock.Mock):
        """ Tests that the call() function works correctly """

        format_TerminalLine.return_value.width = 21
        line = format.TerminalLine()

        repos = [
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/1'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/2'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/3'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/4'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/5'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/6'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/7'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/8'),
            description.RepositoryDescription(
                '/path/to/source', '/path/to/clone/9')
        ]

        expected = list(map(lambda d: d.local.path, repos))

        # create a command object
        cmd = commands.Command(line, repos)

        # a non-plain command
        with unittest.mock.patch('GitManager.commands.Command.PLAIN',
                                 False):

            # run the command
            self.assertEqual(cmd(), len(expected))

            # each of the commands should have been called
            for (e, r) in zip(expected, repos):
                command_write_path_with_counter.assert_any_call(e)
                command_run.assert_any_call(r)

            # it should have been cleaned afterwards
            format_TerminalLine.return_value.clean.assert_called_with()

        # reset all the mocks
        command_run.reset_mock()
        command_write_path_with_counter.reset_mock()
        format_TerminalLine.reset_mock()

        # a plain command
        with unittest.mock.patch('GitManager.commands.Command.PLAIN',
                                 True):
            # run the command
            self.assertEqual(cmd(), len(expected))

            # assert that no path has been printed
            command_write_path_with_counter.assert_not_called()

            # each of the commands should have been called
            for r in repos:
                command_run.assert_any_call(r)

            # it should have been cleaned afterwards
            format_TerminalLine.return_value.clean.assert_called_with()
