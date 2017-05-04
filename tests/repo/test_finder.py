import unittest
import unittest.mock

from GitManager.repo import finder, description


class TestFinder(unittest.TestCase):
    """ Tests that the Finder() class works correctly """

    @unittest.mock.patch("os.listdir")
    @unittest.mock.patch("os.path")
    @unittest.mock.patch("GitManager.repo.finder.Finder.get_from_path")
    def test_find_recursive(self,
                            Finder_get_from_path: unittest.mock.Mock,
                            os_path: unittest.mock.Mock,
                            os_listdir: unittest.mock.Mock):
        """ Tests that the find_recursive method works correctly """

        # Setup all the mocks
        links = ['/link']
        dirs = ['/link', '/link/a', '/link/b', '/folder', '/folder/a',
                '/folder/b']
        listings = {
            '/': ['link', 'file.txt', 'folder', 'folder.txt'],
            '/link': ['a', 'a.txt', 'b', 'b.txt'],
            '/link/a': [],
            '/link/b': [],
            '/folder': ['a', 'a.txt', 'b', 'b.txt'],
            '/folder/a': [],
            '/folder/b': [],
        }
        repos = {
            '/link/a': 'git@example.com:link/a',
            '/link/b': 'git@example.com:link/b',
            '/folder': 'git@example.com:folder',
            '/folder/a': 'git@example.com:folder/a',
            '/folder/b': 'git@example.com:folder/b',
        }

        def join_mock(*args):
            return '/'.join(args).replace('//', '/')

        os_path.islink.side_effect = lambda l: l in links
        os_path.isdir.side_effect = lambda d: d in dirs
        os_listdir.side_effect = lambda d: listings[d]
        os_path.join.side_effect = join_mock

        def frompath_mock(path):
            if path in repos:
                return description.RepositoryDescription(repos[path], path)
            else:
                raise ValueError()

        Finder_get_from_path.side_effect = frompath_mock

        # finding repositories not allowing links and not allowing
        # sub-repositories
        self.assertEqual(list(finder.Finder.
                              find_recursive('/', allow_links=False,
                                             continue_in_repository=False)),
                         [
                             description.RepositoryDescription(
                                 'git@example.com:folder',
                                 '/folder'
                             )
                         ])

        # finding repositories allowing links but not more
        self.assertEqual(list(finder.Finder.
                              find_recursive('/', allow_links=True,
                                             continue_in_repository=False)),
                         [
                             description.RepositoryDescription(
                                 'git@example.com:link/a',
                                 '/link/a'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:link/b',
                                 '/link/b'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:folder',
                                 '/folder'
                             )
                         ])

        # finding repositories allowing repos in repos, but not more
        self.assertEqual(list(finder.Finder.
                              find_recursive('/', allow_links=False,
                                             continue_in_repository=True)),
                         [
                             description.RepositoryDescription(
                                 'git@example.com:folder',
                                 '/folder'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:folder/a',
                                 '/folder/a'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:folder/b',
                                 '/folder/b'
                             )
                         ])

        # finding repositories allow repos in repos and links
        self.assertEqual(list(finder.Finder.
                              find_recursive('/', allow_links=True,
                                             continue_in_repository=True)),
                         [
                             description.RepositoryDescription(
                                 'git@example.com:link/a',
                                 '/link/a'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:link/b',
                                 '/link/b'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:folder',
                                 '/folder'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:folder/a',
                                 '/folder/a'
                             ),
                             description.RepositoryDescription(
                                 'git@example.com:folder/b',
                                 '/folder/b'
                             )
                         ])

    @unittest.mock.patch("GitManager.repo.implementation.LocalRepository")
    def test_get_from_path(self,
                           implementation_LocalRepository: unittest.mock.Mock):
        """ Tests that the get_from_path function works properly """

        # if there is no local repository, we should throw a value error
        implementation_LocalRepository.return_value.exists.return_value = False

        with self.assertRaises(ValueError):
            finder.Finder.get_from_path('/path/to/repository')

        implementation_LocalRepository.assert_called_with(
            '/path/to/repository')

        # reset the mocks
        implementation_LocalRepository.reset_mock()

        # local repository exists, and the return
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.get_remote_url \
            .return_value = 'git@example.com:example/repo'

        # check that a repository with an origin is found properly
        self.assertEqual(
            finder.Finder.get_from_path('/path/to/repository'),
            description.RepositoryDescription(
                'git@example.com:example/repo',
                '/path/to/repository'
            )
        )

        implementation_LocalRepository.assert_called_with(
            '/path/to/repository')
        implementation_LocalRepository.return_value.get_remote_url \
            .assert_called_with('origin')

        # reset the mocks
        implementation_LocalRepository.reset_mock()

        def mock_raise(arg):
            raise ValueError()

        # raises an error if no url is returned
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remotes = []
        implementation_LocalRepository.return_value.get_remote_url \
            .side_effect = mock_raise

        # check that a repository
        with self.assertRaises(ValueError):
            finder.Finder.get_from_path('/path/to/repository')

        implementation_LocalRepository.return_value.get_remote_url \
            .assert_called_with('origin')

        # reset the mocks
        implementation_LocalRepository.reset_mock()

        # raises an error if no url is returned
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remotes = ['upstream']
        implementation_LocalRepository.return_value.get_remote_url \
            .side_effect = mock_raise

        # check that a repository
        with self.assertRaises(ValueError):
            finder.Finder.get_from_path('/path/to/repository')

        implementation_LocalRepository.return_value.get_remote_url \
            .assert_any_call('origin')

        implementation_LocalRepository.return_value.get_remote_url \
            .assert_any_call('upstream')

        # reset the mocks
        implementation_LocalRepository.reset_mock()

        def mock_originerror(name):
            if name == 'origin':
                raise ValueError()
            else:
                return 'git@example.com:example/repo'

        # raises an error if no url is returned
        implementation_LocalRepository.return_value.exists.return_value = True
        implementation_LocalRepository.return_value.remotes = ['upstream']
        implementation_LocalRepository.return_value.get_remote_url \
            .side_effect = mock_originerror

        # check that a repository with an upstream is found properly
        self.assertEqual(
            finder.Finder.get_from_path('/path/to/repository'),
            description.RepositoryDescription(
                'git@example.com:example/repo',
                '/path/to/repository'
            )
        )

        implementation_LocalRepository.return_value.get_remote_url \
            .assert_any_call('origin')

        implementation_LocalRepository.return_value.get_remote_url \
            .assert_any_call('upstream')
