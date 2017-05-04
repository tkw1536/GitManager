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
            self.assertEqual(actual,
                             (i + 1, intended), "Lines parsed properly")

        # reset the lines to something that should thrown an error
        t.lines = [
            line.BaseLine('', 2, ' ', 'something', '')
        ]

        # we are skipping a base level -- this should thrown an error
        with self.assertRaises(Exception):
            list(t.repositories)

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
            list(t.repositories)

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
            list(t.locals)

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_index(self, os_path_expanduser: unittest.mock.Mock):
        """ Tests that the index function works properly """

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

        # check that the indexes are found properly
        for (i, r) in enumerate(results):
            self.assertEqual(t.index(r), i + 1, "Lines found as intended")

        self.assertEqual(t.index(d.BaseDescription('/path/to/home/weird')),
                         None,
                         "Lines not found as intended")

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_contains(self, os_path_expanduser: unittest.mock.Mock):
        """ Tests that the contains function works properly """

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

        # check that the indexes are found properly
        for (i, r) in enumerate(results):
            self.assertTrue(t.contains(r), "Lines found as intended")

        self.assertFalse(t.contains(d.BaseDescription('/path/to/home/weird')),
                         "Lines not found as intended")

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_insert_at(self, os_path_expanduser: unittest.mock.Mock):
        """ Tests that the contains function works properly """

        def setup_tree() -> tree.Tree:
            # create a tree instance and setup lines
            t = tree.Tree()
            t.lines = [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]

            return t

        #
        # INSERT FAILURES -- for RepositoryDescriptions
        #

        t1 = setup_tree()

        # Inserting into something that doesn't exist throws a ValueError
        with self.assertRaises(ValueError):
            t1.insert_at(
                d.BaseDescription('/path/to/home/else'),
                d.RepositoryDescription(source='git@example.com:/example/repo',
                                        path='/path/to/home/else/hello')
            )

        t2 = setup_tree()

        # Inserting into the wrong parent also throws ValueError
        with self.assertRaises(ValueError):
            t2.insert_at(
                d.BaseDescription('/path/to/home/else'),
                d.RepositoryDescription(source='git@example.com:/example/repo',
                                        path='/path/to/home/weird/hello')
            )

        t3 = setup_tree()

        # Inserting into the wrong parent also throws ValueError
        with self.assertRaises(ValueError):
            t2.insert_at(
                None,
                d.RepositoryDescription(source='git@example.com:/example/repo',
                                        path='/path/to/home/weird/hello')
            )

        #
        # INSERT SUCCESS -- for RepositoryDescriptions
        #

        t4 = setup_tree()
        d4 = d.RepositoryDescription(
            source='git@example.com:/example/insertion',
            path='/path/to/home/insertion')

        # at the very top
        self.assertEqual(t4.insert_at(None, d4), 1, 'Inserting a repository '
                                                    'top-level')
        self.assertEqual(t4.lines, [
            line.NOPLine("# comment"),
            line.RepoLine(' ', 'git@example.com:/example/insertion', '', '',
                          ''),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', '')
        ])

        # inside of an empty group
        t5 = setup_tree()
        d5 = d.RepositoryDescription(
            source='git@example.com:/example/insertion',
            path='/path/to/home/base1/insertion')
        p5 = d.BaseDescription('/path/to/home/base1')

        self.assertEqual(t5.insert_at(p5, d5), 2, 'Inserting a repository '
                                                  'into an empty group')
        self.assertEqual(t5.lines, [
            line.NOPLine("# comment"),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.RepoLine('  ', 'git@example.com:/example/insertion', '', '',
                          ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', '')
        ])

        # inside of a full group
        t6 = setup_tree()
        d6 = d.RepositoryDescription(
            source='git@example.com:/example/insertion',
            path='/path/to/home/base2/point')
        p6 = d.BaseDescription('/path/to/home/base2')

        self.assertEqual(t6.insert_at(p6, d6), 4, 'Inserting a repository '
                                                  'into a full group')
        self.assertEqual(t6.lines, [
            line.NOPLine("# comment"),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', ''),
            line.RepoLine('  ', 'git@example.com:/example/insertion', ' ',
                          'point', ''),
        ])

        #
        # INSERT SUCCESS -- for BaseDescriptions
        #

        t7 = setup_tree()
        d7 = d.BaseDescription('/path/to/home/insertion')

        # at the very top
        self.assertEqual(t7.insert_at(None, d7), 4, 'Inserting a base '
                                                    'top-level')

        self.assertEqual(t7.lines, [
            line.NOPLine("# comment"),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', ''),
            line.BaseLine(' ', 1, ' ', 'insertion', '')
        ])

        # inside of an empty group
        t8 = setup_tree()
        d8 = d.BaseDescription('/path/to/home/base1/insertion')
        p8 = d.BaseDescription('/path/to/home/base1')

        self.assertEqual(t8.insert_at(p8, d8), 2, 'Inserting a base '
                                                  'into an empty group')
        self.assertEqual(t8.lines, [
            line.NOPLine("# comment"),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.BaseLine('  ', 2, ' ', 'insertion', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', '')
        ])

        # inside of a full group
        t9 = setup_tree()
        d9 = d.BaseDescription('/path/to/home/base2/insertion')
        p9 = d.BaseDescription('/path/to/home/base2')

        self.assertEqual(t9.insert_at(p9, d9), 4, 'Inserting a base '
                                                  'into a full group')
        self.assertEqual(t9.lines, [
            line.NOPLine("# comment"),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', ''),
            line.BaseLine('  ', 2, ' ', 'insertion', ''),
        ])

        # inside of a full group
        t10 = setup_tree()
        d10 = d.BaseDescription('/insertion')
        p10 = d.BaseDescription('/path/to/home/base2')

        self.assertEqual(t10.insert_at(p10, d10), 4, 'Inserting a base with'
                                                     'absolute path')

        self.assertEqual(t10.lines, [
            line.NOPLine("# comment"),
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', ''),
            line.BaseLine('  ', 2, ' ', '/insertion', ''),
        ])

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_insert_base_or_get(self, os_path_expanduser: unittest.mock.Mock):

        def setup_tree() -> tree.Tree:
            # create a tree instance and setup lines
            t = tree.Tree()
            t.lines = [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]

            return t

        # inserting an existing base -- do nothing
        t1 = setup_tree()
        d1 = d.BaseDescription('/path/to/home/base1')

        self.assertEqual(t1.insert_base_or_get(d1), 1, 'inserting an '
                                                       'existing base')

        self.assertEqual(
            t1.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]
        )

        # inserting a new base top-level
        t2 = setup_tree()
        d2 = d.BaseDescription('/path/to/home/base3')

        self.assertEqual(t2.insert_base_or_get(d2), 4, 'inserting a new '
                                                       'top-level base')

        self.assertEqual(
            t2.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', ''),
                line.BaseLine(' ', 1, ' ', 'base3', '')
            ]
        )

        # inserting an absolute path
        t3 = setup_tree()
        d3 = d.BaseDescription('/base3')

        self.assertEqual(t3.insert_base_or_get(d3), 4, 'inserting a new '
                                                       'absolute-path base')

        self.assertEqual(
            t3.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', ''),
                line.BaseLine(' ', 1, ' ', '/base3', '')
            ]
        )

        # inserting a single sublevel
        t4 = setup_tree()
        d4 = d.BaseDescription('/path/to/home/base1/a')

        self.assertEqual(t4.insert_base_or_get(d4), 2, 'inserting a single '
                                                       'new sub-level base')

        self.assertEqual(
            t4.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine('  ', 2, ' ', 'a', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]
        )

        # inserting multiple sublevels
        t5 = setup_tree()
        d5 = d.BaseDescription('/path/to/home/base1/a/b/c')

        self.assertEqual(t5.insert_base_or_get(d5), 4, 'inserting multiple '
                                                       'new sub-level bases')

        self.assertEqual(
            t5.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine('  ', 2, ' ', 'a', ''),
                line.BaseLine('   ', 3, ' ', 'b', ''),
                line.BaseLine('    ', 4, ' ', 'c', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', ''),
            ]
        )

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_insert_repo_or_get(self, os_path_expanduser: unittest.mock.Mock):

        def setup_tree() -> tree.Tree:
            # create a tree instance and setup lines
            t = tree.Tree()
            t.lines = [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]

            return t

        # inserting an existing repo -- do nothing
        t1 = setup_tree()
        d1 = d.RepositoryDescription('git@example.com:/example/repo',
                                     '/path/to/home/base2/example-repo')

        self.assertEqual(t1.insert_repo_or_get(d1), 3, 'inserting an '
                                                       'existing repo')

        self.assertEqual(
            t1.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]
        )

        # inserting a new repo top-level
        t2 = setup_tree()
        d2 = d.RepositoryDescription('git@example.com:/example/insert',
                                     '/path/to/home/insert')

        self.assertEqual(t2.insert_repo_or_get(d2), 1, 'inserting a new '
                                                       'top-level repo')

        self.assertEqual(
            t2.lines,
            [
                line.NOPLine("# comment"),
                line.RepoLine(' ', 'git@example.com:/example/insert', '',
                              '', ''),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', '')
            ]
        )

        # inserting a new repo with multiple sublevels
        t5 = setup_tree()
        d5 = d.RepositoryDescription('git@example.com:/example/insert',
                                     '/path/to/home/base1/a/b/c/insert')

        self.assertEqual(t5.insert_repo_or_get(d5), 5, 'inserting a new '
                                                       'repo and sub-levels')

        self.assertEqual(
            t5.lines,
            [
                line.NOPLine("# comment"),
                line.BaseLine(' ', 1, ' ', 'base1', ''),
                line.BaseLine('  ', 2, ' ', 'a', ''),
                line.BaseLine('   ', 3, ' ', 'b', ''),
                line.BaseLine('    ', 4, ' ', 'c', ''),
                line.RepoLine('     ', 'git@example.com:/example/insert',
                              '', '', ''),
                line.BaseLine(' ', 1, ' ', 'base2', ''),
                line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                              'example-repo', ''),
            ]
        )

    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_rebuild(self, os_path_expanduser: unittest.mock.Mock):

        # create a tree instance and setup lines
        t = tree.Tree()
        t.lines = [
            line.NOPLine("# comment"),
            line.BaseLine('    ', 1, ' ', 'base1', ''),
            line.RepoLine('        ', 'git@example.com:/example/repo', ' ',
                          'example-repo', ''),
            line.BaseLine('      ', 1, ' ', 'base2', ''),
            line.RepoLine('        ', 'git@example.com:/example/repo', ' ',
                          'example-repo', '')
        ]

        t.rebuild()

        self.assertEqual(t.lines, [
            line.BaseLine(' ', 1, ' ', 'base1', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', ''),
            line.BaseLine(' ', 1, ' ', 'base2', ''),
            line.RepoLine('  ', 'git@example.com:/example/repo', ' ',
                          'example-repo', '')
        ])
