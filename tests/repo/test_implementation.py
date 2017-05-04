import unittest
import unittest.mock

from GitManager.repo import implementation


class TestLocalRepository(unittest.TestCase):
    def test_eq(self):
        """ Checks that equality between LocalRepositories works properly """

        self.assertEqual(
            implementation.LocalRepository('/path/to/clone'),
            implementation.LocalRepository('/path/to/clone'),
            'equality between two LocalRepositories'
        )

        self.assertNotEqual(
            implementation.LocalRepository('/home/user/example'),
            implementation.LocalRepository(
                '/home/user/example/.git'),
            'difference between two LocalRepositories')

    def test_path(self):
        """ Tests that the path property works as intended """

        self.assertEqual(
            implementation.LocalRepository('/path/to/clone').path,
            '/path/to/clone',
            'path of a simple repository'
        )

        self.assertEqual(
            implementation.LocalRepository(
                '/home/user/example').path,
            '/home/user/example',
            'path of a simple git repository'
        )

    def test_str(self):
        """ Tests that the str() of a remoteRepository works properly """

        self.assertEqual(
            str(implementation.LocalRepository(
                '/path/to/clone')),
            '/path/to/clone',
            'str() of a simple repository'
        )

        self.assertEqual(
            str(implementation.LocalRepository(
                '/home/user/example')),
            '/home/user/example',
            'str() of a simple git repository'
        )

    def test_repr(self):
        """ Tests that the repr() of a remoteRepository works properly """

        self.assertEqual(
            repr(implementation.LocalRepository(
                '/path/to/clone')),
            '<LocalRepository /path/to/clone>',
            'str() of a simple repository'
        )

        self.assertEqual(
            repr(implementation.LocalRepository(
                '/home/user/example')),
            '<LocalRepository /home/user/example>',
            'repr() of a simple git repository'
        )

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_remotes(self, run_gitrun: unittest.mock.Mock):
        """ checks that remotes properly works as intended """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # set the return value
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="origin\nupstream".encode("utf-8"))()

        self.assertEqual(repo.remotes, ["origin", "upstream"], "Remotes are "
                                                               "parsed "
                                                               "properly")

        run_gitrun.assert_called_with('remote', 'show', '-n',
                                      cwd='/path/to/repository')
        run_gitrun.return_value.wait.assert_called_with()

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_get_remote_url(self, run_gitrun: unittest.mock.Mock):
        """ checks that get_remote_url function works as intended """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # throw an error for the remote
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="fatal: No such remote 'example'\n".encode("utf-8"))()
        run_gitrun.return_value.success = False

        # check that an error is thrown if we look for a remote that doesn't
        # exist
        with self.assertRaises(ValueError):
            repo.get_remote_url("example")

        run_gitrun.assert_called_with('remote', 'get-url', 'example',
                                      cwd='/path/to/repository')

        # thrown no error
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="git@example.com:example/repo\n".encode("utf-8"))()
        run_gitrun.return_value.success = True

        # check that we can actually get the remote url
        self.assertEqual(repo.get_remote_url('origin'),
                         'git@example.com:example/repo', 'getting a remote '
                                                         'url')

        # check that the git run has been called
        run_gitrun.assert_called_with('remote', 'get-url', 'origin',
                                      cwd='/path/to/repository')

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    @unittest.mock.patch('os.path.isdir')
    def test_exists(self, os_path_isdir: unittest.mock.Mock,
                    run_gitrun: unittest.mock.Mock):
        """ checks that exists method makes an external call """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # setup mocks so that the path does not exist
        os_path_isdir.return_value = False

        self.assertFalse(repo.exists(), 'non-existence of a repository')

        os_path_isdir.assert_called_with('/path/to/repository')
        run_gitrun.assert_not_called()

        # setup mocks so that the path exists but the --show-toplevel fails
        os_path_isdir.reset_mock()
        os_path_isdir.return_value = True

        run_gitrun.reset_mock()
        run_gitrun.return_value.success = False
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="/path/to\n".encode("utf-8"))()

        self.assertFalse(repo.exists(),
                         'non-existence of a repository when toplevel fails')

        os_path_isdir.assert_called_with('/path/to/repository')
        run_gitrun.assert_called_with('rev-parse', '--show-toplevel',
                                      cwd='/path/to/repository')

        run_gitrun.reset_mock()
        run_gitrun.return_value.success = True
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="/path/to\n".encode("utf-8"))()

        self.assertFalse(repo.exists(),
                         'non-existence of a repository when not toplevel')

        os_path_isdir.assert_called_with('/path/to/repository')
        run_gitrun.assert_called_with('rev-parse', '--show-toplevel',
                                      cwd='/path/to/repository')

        # setup mocks so that the path exists and is toplevel
        os_path_isdir.reset_mock()
        os_path_isdir.return_value = True

        run_gitrun.reset_mock()
        run_gitrun.return_value.success = True
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="/path/to/repository\n".encode("utf-8"))()

        self.assertTrue(repo.exists(),
                        'existence of a repository when not toplevel')

        os_path_isdir.assert_called_with('/path/to/repository')
        run_gitrun.assert_called_with('rev-parse', '--show-toplevel',
                                      cwd='/path/to/repository')

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_ref_parse(self, run_gitrun: unittest.mock.Mock):
        """ checks that ref_parse function works as intended """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # set the return value
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="aaaaaa\n".encode("utf-8"))()

        self.assertEqual(repo.ref_parse("master"), "aaaaaa", "parsing master "
                                                             "works properly")

        run_gitrun.assert_called_with("rev-parse", "master",
                                      cwd='/path/to/repository')
        run_gitrun.return_value.wait.assert_called_with()

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_symbolic_ref(self, run_gitrun: unittest.mock.Mock):
        """ checks that symbolic_ref properly works as intended """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # set the return value
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="refs/heads/master\n".encode("utf-8"))()

        self.assertEqual(repo.symbolic_ref("HEAD"), "refs/heads/master",
                         "parsing symbolic ref works properly")

        run_gitrun.assert_called_with("symbolic-ref", "-q", "HEAD",
                                      cwd='/path/to/repository')
        run_gitrun.return_value.wait.assert_called_with()

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_upstream_ref(self, run_gitrun: unittest.mock.Mock):
        """ checks that upstream_ref properly works as intended """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # set the return value
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="origin/master\n".encode("utf-8"))()

        self.assertEqual(repo.upstream_ref("refs/heads/master"),
                         "origin/master",
                         "parsing upstream ref works properly")

        run_gitrun.assert_called_with("for-each-ref",
                                      "--format=%(upstream:short)",
                                      "refs/heads/master",
                                      cwd='/path/to/repository')
        run_gitrun.return_value.wait.assert_called_with()

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_fetch(self, run_gitrun: unittest.mock.Mock):
        """ checks that fetch method makes an external call """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # and make sure that the return value is True
        run_gitrun.success = True

        # assert that we can fetch
        self.assertTrue(repo.fetch(), 'fetching a repository')

        # check that we called the fetch --all command properly
        run_gitrun.assert_called_with('fetch', '--all', '--quiet',
                                      cwd='/path/to/repository',
                                      pipe_stderr=True, pipe_stdin=True,
                                      pipe_stdout=True)

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_pull(self, run_gitrun: unittest.mock.Mock):
        """ checks that pull method makes an external call """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # and make sure that the return value is True
        run_gitrun.success = True

        # assert that we can pull
        self.assertTrue(repo.pull(), 'pulling a repository')

        # check that we called the pull command properly
        run_gitrun.assert_called_with('pull', cwd='/path/to/repository',
                                      pipe_stderr=True, pipe_stdin=True,
                                      pipe_stdout=True)

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_push(self, run_gitrun: unittest.mock.Mock):
        """ checks that push method makes an external call """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # and make sure that the return value is True
        run_gitrun.success = True

        # assert that we can push
        self.assertTrue(repo.push(), 'push a repository')

        # check that we called the push command properly
        run_gitrun.assert_called_with('push', cwd='/path/to/repository',
                                      pipe_stderr=True, pipe_stdin=True,
                                      pipe_stdout=True)

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_local_status(self, run_gitrun: unittest.mock.Mock):
        """ checks that local_status method makes an external call """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # mock the exists function
        repo.exists = unittest.mock.MagicMock(return_value=False)

        # local status and non-existence
        self.assertEqual(repo.local_status(), None, "local_status of "
                                                    "non-existing "
                                                    "repository")

        # reset the mock and change the return value to True
        repo.exists.reset_mock()
        repo.exists.return_value = True

        # setup the return value of the git run
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="".encode("utf-8"))()

        # check that the local_status did print correctly
        self.assertEqual(repo.local_status(), "", "Reading status works "
                                                  "properly")

        # check that we called the status command
        run_gitrun.assert_called_with('status', '--porcelain',
                                      cwd='/path/to/repository')

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository.ref_parse',
        side_effect=["aaaaaa", "bbbbbb", "aaaaaa", "bbbbbb", "aaaaaa",
                     "bbbbbb", "aaaaaa", "bbbbbb", "aaaaaa", "bbbbbb"]
    )
    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository.upstream_ref',
        side_effect=["origin/master", "origin/master", "origin/master",
                     "origin/master", "origin/master"]
    )
    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository.symbolic_ref',
        side_effect=["refs/heads/master", "refs/heads/master",
                     "refs/heads/master", "refs/heads/master",
                     "refs/heads/master"]
    )
    @unittest.mock.patch(
        'GitManager.repo.implementation.LocalRepository.exists'
    )
    def test_remote_status(self,
                           LocalRepository_exists: unittest.mock.Mock,
                           LocalRepository_symbolic_ref: unittest.mock.Mock,
                           LocalRepository_upstream_ref: unittest.mock.Mock,
                           LocalRepository_ref_parse: unittest.mock.Mock,
                           run_gitrun: unittest.mock.Mock):
        """ Tests that the remote_status command works properly """

        # create a repository
        repo = implementation.LocalRepository('/path/to/repository')

        # if we want to update, we should have called with 'remote' 'update'
        run_gitrun.return_value.success = False
        self.assertEqual(repo.remote_status(update=True), None)
        run_gitrun.assert_called_with('remote', 'update',
                                      cwd='/path/to/repository')

        # reset all the mocks
        LocalRepository_exists.reset_mock()
        LocalRepository_symbolic_ref.reset_mock()
        LocalRepository_upstream_ref.reset_mock()
        LocalRepository_ref_parse.reset_mock()
        run_gitrun.reset_mock()
        run_gitrun.return_value.success = True

        # merge base is aaaaaa (local)
        LocalRepository_exists.return_value = False
        self.assertEqual(repo.remote_status(), None)

        # reset all the mocks
        LocalRepository_exists.reset_mock()
        LocalRepository_symbolic_ref.reset_mock()
        LocalRepository_upstream_ref.reset_mock()
        LocalRepository_ref_parse.reset_mock()
        run_gitrun.reset_mock()

        # merge base is local
        LocalRepository_exists.return_value = True
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="aaaaaa\n".encode("utf-8"))()

        self.assertEqual(repo.remote_status(update=False),
                         implementation.RemoteStatus.REMOTE_NEWER)
        run_gitrun.assert_called_with("merge-base", "aaaaaa", "bbbbbb",
                                      cwd="/path/to/repository")
        # reset all the mocks
        LocalRepository_exists.reset_mock()
        LocalRepository_symbolic_ref.reset_mock()
        LocalRepository_upstream_ref.reset_mock()
        LocalRepository_ref_parse.reset_mock()
        run_gitrun.reset_mock()

        # merge base is local
        LocalRepository_exists.return_value = True
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="bbbbbb\n".encode("utf-8"))()

        self.assertEqual(repo.remote_status(),
                         implementation.RemoteStatus.LOCAL_NEWER)
        run_gitrun.assert_called_with("merge-base", "aaaaaa", "bbbbbb",
                                      cwd="/path/to/repository")

        # reset all the mocks
        LocalRepository_exists.reset_mock()
        LocalRepository_symbolic_ref.reset_mock()
        LocalRepository_upstream_ref.reset_mock()
        LocalRepository_ref_parse.reset_mock()
        run_gitrun.reset_mock()

        # merge base is ????
        LocalRepository_exists.return_value = True
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="cccccc\n".encode("utf-8"))()

        self.assertEqual(repo.remote_status(update=False),
                         implementation.RemoteStatus.DIVERGENCE)
        run_gitrun.assert_called_with("merge-base", "aaaaaa", "bbbbbb",
                                      cwd="/path/to/repository")

        # reset all the mocks
        LocalRepository_exists.reset_mock()
        LocalRepository_symbolic_ref.reset_mock()
        LocalRepository_upstream_ref.reset_mock()
        LocalRepository_ref_parse.reset_mock()
        run_gitrun.reset_mock()

        # both refs are equal
        LocalRepository_ref_parse.side_effect = ["aaaaaa", "aaaaaa"]
        LocalRepository_exists.return_value = True
        run_gitrun.return_value.stdout = unittest.mock.mock_open(
            read_data="aaaaaa\n".encode("utf-8"))()

        self.assertEqual(repo.remote_status(update=False),
                         implementation.RemoteStatus.UP_TO_DATE)
        run_gitrun.assert_called_with("merge-base", "aaaaaa", "aaaaaa",
                                      cwd="/path/to/repository")


class TestRemoteRepository(unittest.TestCase):
    """ Tests that implementation works properly """

    def test_eq(self):
        """ Checks that equality between RemoteRepositories works properly """

        self.assertEqual(
            implementation.RemoteRepository('git@github.com:hello/world.git'),
            implementation.RemoteRepository('git@github.com:hello/world.git'),
            'equality between two RemoteRepositories'
        )

        self.assertNotEqual(
            implementation.RemoteRepository('git@github.com:hello/world.git'),
            implementation.RemoteRepository(
                'https://github.com/hello/world.git'),
            'difference between two RemoteRepositories'
        )

    def test_url(self):
        """ Tests that the URL property works as intended """

        self.assertEqual(
            implementation.RemoteRepository(
                'git@github.com:hello/world.git').url,
            'git@github.com:hello/world.git',
            'URL of a simple repository'
        )

        self.assertEqual(
            implementation.RemoteRepository(
                'https://github.com/hello/world.git').url,
            'https://github.com/hello/world.git',
            'URL of a simple git repository'
        )

    def test_str(self):
        """ Tests that the str() of a remoteRepository works properly """

        self.assertEqual(
            str(implementation.RemoteRepository(
                'git@github.com:hello/world.git')),
            'git@github.com:hello/world.git',
            'str() of a simple repository'
        )

        self.assertEqual(
            str(implementation.RemoteRepository(
                'https://github.com/hello/world.git')),
            'https://github.com/hello/world.git',
            'str() of a simple git repository'
        )

    def test_repr(self):
        """ Tests that the repr() of a remoteRepository works properly """

        self.assertEqual(
            repr(implementation.RemoteRepository(
                'git@github.com:hello/world.git')),
            '<RemoteRepository git@github.com:hello/world.git>',
            'str() of a simple repository'
        )

        self.assertEqual(
            repr(implementation.RemoteRepository(
                'https://github.com/hello/world.git')),
            '<RemoteRepository https://github.com/hello/world.git>',
            'repr() of a simple git repository'
        )

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_exists(self, run_gitrun: unittest.mock.Mock):
        """ checks that exists method makes an external call """

        run_gitrun.return_value.success = True

        # checking for existence should make an external call
        self.assertTrue(implementation.RemoteRepository(
            'git@github.com:hello/world.git').exists(),
                        'successfully checks existence using an external call')

        run_gitrun.assert_called_with('ls-remote', '--exit-code',
                                      'git@github.com:hello/world.git')

    @unittest.mock.patch('GitManager.utils.run.GitRun')
    def test_clone(self, run_gitrun: unittest.mock.Mock):
        """ checks that clone method makes an external call """

        run_gitrun.return_value.success = True

        remote = implementation.RemoteRepository(
            'git@github.com:hello/world.git')
        local = implementation.LocalRepository('/path/to/clone')

        # checking for existence should make an external call
        self.assertTrue(remote.clone(local), 'successfully clones a '
                                             'repository')

        run_gitrun.assert_called_with('clone',
                                      'git@github.com:hello/world.git',
                                      '/path/to/clone', pipe_stderr=True,
                                      pipe_stdin=True, pipe_stdout=True)

    def test_humanish_part(self):
        """ Checks that the get_humanish_part method works properly"""

        self.assertEqual(
            implementation.RemoteRepository(
                'git@github.com:hello/world.git').humanish_part(),
            'world')

        self.assertEqual(
            implementation.RemoteRepository(
                'git@github.com:hello/world').humanish_part(),
            'world'
        )

        self.assertEqual(
            implementation.RemoteRepository(
                'git@github.com:hello/world/').humanish_part(),
            'world'
        )

        self.assertEqual(
            implementation.RemoteRepository(
                'git@github.com:hello/world//').humanish_part(),
            'world'
        )
