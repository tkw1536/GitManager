import unittest
import unittest.mock

from GitManager.config import line
from GitManager.repo import description, implementation


class TestBaseDescription(unittest.TestCase):
    """ Tests that the BaseDescription class works properly """

    def test_eq(self):
        """ Tests that equality works properly """

        self.assertEqual(
            description.BaseDescription('/path/to/local'),
            description.BaseDescription('/path/to/local'),
            'equality between two descriptions'
        )

        self.assertNotEqual(
            description.BaseDescription('/path/to/local/a'),
            description.BaseDescription('/path/to/local/b'),
            'inequality between two descriptions'
        )


class TestRepositoryDescription(unittest.TestCase):
    """ Tests that the RepositoryDescription class works properly """

    def test_eq(self):
        """ Tests that equality works properly """

        self.assertEqual(description.RepositoryDescription(
            'git@github.com:/example/remote',
            '/path/to/local'),
            description.RepositoryDescription(
                'git@github.com:/example/remote',
                '/path/to/local'),
            'equality between two descriptions'
        )

        self.assertNotEqual(description.RepositoryDescription(
            'git@github.com:/example/remote',
            '/path/to/local'),
            description.RepositoryDescription(
                'github.com:/example/remote',
                '/path/to/local'),
            'inequality between two descriptions'
        )

    def test_local(self):
        """ Tests that local repositories are parsed properly """

        self.assertEqual(description.RepositoryDescription(
            'git@github.com:/example/remote', '/path/to/local').local,
                         implementation.LocalRepository('/path/to/local'))

    def test_remote(self):
        """ Tests that the remote repositories are parsed properly """

        self.assertEqual(description.RepositoryDescription(
            'git@github.com:/example/remote', '/path/to/local').remote,
                         implementation.RemoteRepository(
                             'git@github.com:/example/remote'))

    def test_to_repo_line(self):
        desc1 = description.RepositoryDescription(
            'git@github.com:/example/remote/repo', '/path/to/local/repo')

        res1 = (
            description.BaseDescription('/path/to/local'),
            line.RepoLine(
                ' ', 'git@github.com:/example/remote/repo', '', '', '   '
            )
        )

        self.assertEqual(desc1.to_repo_line(' ', '  ', '   '), res1,
                         'turning a RepositoryDescription into a RepoLine '
                         'omitting final component')

        desc2 = description.RepositoryDescription(
            'git@github.com:/example/remote/repo', '/path/to/local/repo/clone')

        res2 = (
            description.BaseDescription('/path/to/local/repo'),
            line.RepoLine(
                ' ', 'git@github.com:/example/remote/repo', '  ', 'clone',
                '   '
            )
        )

        self.assertEqual(desc2.to_repo_line(' ', '  ', '   '), res2,
                         'turning a RepositoryDescription into a RepoLine '
                         'including final component')
