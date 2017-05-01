import unittest
import unittest.mock

from GitManager.repo import description, implementation


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
