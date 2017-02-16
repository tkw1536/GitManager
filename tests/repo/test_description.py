import unittest
import unittest.mock

from GitManager.repo import description, implementation


class TestDescription(unittest.TestCase):
    """ Tests that the description class works properly """

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
