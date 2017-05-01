import unittest
import unittest.mock

from GitManager.config import tree, line
from GitManager.repo import description as d
from GitManager.repo.implementation import LocalRepository


class TestTree(unittest.TestCase):
    """ Tests that Tree() can be correctly parsed and changed """

    def test_lines(self):
        """ Test that the lines are correctly initialised """

        t = tree.Tree()

        self.assertEqual(t.lines, [], "by default, lines are empty")

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_descriptions(self, os_path_expanduser: unittest.mock.Mock):
        """ Tests that the descriptions are yielded properly """

        # create a tree instance
        t = tree.Tree()

        # setup the lines properly
        t.lines = [
            line.NOPLine("# Top level line with a comment"),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'something', ''),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 2, ' ', 'sub', ''),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'else', ''),
            line.RepoLine(' ', 'hello', ' ', 'world', ' ')
        ]

        # the intended results
        results = [
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/world'),
            d.BaseDescription('/path/to/home/something'),
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/something/world'),
            d.BaseDescription('/path/to/home/something/sub'),
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/something/sub/world'),
            d.BaseDescription('/path/to/home/else'),
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/else/world')
        ]

        # check that the yielding works properly
        for (i, (actual, intended)) in enumerate(zip(t.descriptions, results)):
            self.assertEqual(actual, (i + 1, intended),
                             "Lines parsed properly")

        # reset the lines to something that should thrown an error
        t.lines = [
            line.BaseLine('', 2, ' ', 'something', '')
        ]

        # we are skipping a base level -- this should thrown an error
        with self.assertRaises(Exception):
            for l in t.repositories:
                pass

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_repositories(self, os_path_expanduser: unittest.mock.Mock):
        """ Tests that the repositories are yielded properly """

        # create a tree instance
        t = tree.Tree()

        # setup the lines properly
        t.lines = [
            line.NOPLine("# Top level line with a comment"),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'something', ''),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 2, ' ', 'sub', ''),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'else', ''),
            line.RepoLine(' ', 'hello', ' ', 'world', ' ')
        ]

        # the intended results
        results = [
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/world'),
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/something/world'),
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/something/sub/world'),
            d.RepositoryDescription(source='hello',
                                    path='/path/to/home/else/world')
        ]

        # check that the yielding works properly
        for (actual, intended) in zip(t.repositories, results):
            self.assertEqual(actual, intended, "Lines parsed properly")

        # reset the lines to something that should thrown an error
        t.lines = [
            line.BaseLine('', 2, ' ', 'something', '')
        ]

        # we are skipping a base level -- this should thrown an error
        with self.assertRaises(Exception):
            for l in t.repositories:
                pass

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_locals(self, os_path_expanduser: unittest.mock.Mock):
        """ Tests that the locals are yielded properly """

        # create a tree instance
        t = tree.Tree()

        # setup the lines properly
        t.lines = [
            line.NOPLine("# Top level line with a comment"),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'something', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 2, ' ', 'sub', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'else', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' ')
        ]

        # the intended results
        results = [
            LocalRepository('/path/to/home/world'),
            LocalRepository('/path/to/home/something/world'),
            LocalRepository('/path/to/home/something/sub/world'),
            LocalRepository('/path/to/home/else/world')
        ]

        # check that the yielding works properly
        for (actual, intended) in zip(t.locals, results):
            self.assertEqual(actual, intended, "Locals parsed properly")

        # reset the lines to something that should thrown an error
        t.lines = [
            line.BaseLine('', 2, ' ', 'something', '')
        ]

        # we are skipping a base level -- this should thrown an error
        with self.assertRaises(Exception):
            for l in t.locals:
                pass
