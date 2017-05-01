import unittest
import unittest.mock

from GitManager.config import file, line


class TestFile(unittest.TestCase):
    """ Tests that File() can be correctly read and parsed """

    def test_read(self):
        """ Tests that the locals are yielded properly """

        # read the lines from the configuration file
        fn = file.File("/path/to/config")

        fake_lines = "\n".join([
            "# Top level line with a comment",
            " hello world ",
            "> something ",
            " hello world ",
            ">> sub ",
            " hello world ",
            "> else ",
            " hello world"
        ]).encode("utf-8")

        with unittest.mock.patch('builtins.open',
                                 new_callable=unittest.mock.mock_open(
                                     read_data=fake_lines)) \
                as _:
            # read all the lines
            fn.read()

        expected = [
            line.NOPLine("# Top level line with a comment"),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'something', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 2, ' ', 'sub', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'else', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' ')
        ]

        for (actual, intended) in zip(fn.lines, expected):
            self.assertEqual(actual, intended, "line parsed properly")

    @unittest.mock.patch('builtins.open')
    def test_write(self, builtins_open: unittest.mock.Mock):
        """ Tests that writing lines works properly """

        # create a config file instance
        fn = file.File("/path/to/config")

        # setup the lines properly
        fn.lines = [
            line.NOPLine("# Top level line with a comment"),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'something', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 2, ' ', 'sub', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' '),
            line.BaseLine('', 1, ' ', 'else', ' '),
            line.RepoLine(' ', 'hello', ' ', 'world', ' ')
        ]

        fake_lines = [
            "# Top level line with a comment",
            " hello world ",
            "> something ",
            " hello world ",
            ">> sub ",
            " hello world ",
            "> else ",
            " hello world "
        ]

        # do the writing
        fn.write()

        # check that each of the lines has been written
        for l in fake_lines:
            builtins_open.return_value.__enter__.return_value.write. \
                assert_any_call("{}\n".format(l))

    @unittest.mock.patch('os.path.isfile', return_value=False)
    @unittest.mock.patch('os.path.expanduser',
                         side_effect=lambda s: s.replace("~",
                                                         "/path/to/home/"))
    def test_find(self, os_path_expanduser: unittest.mock.Mock,
                  os_path_isfile: unittest.mock.Mock):
        """ Tests that the find() method works properly """

        # no environment variables
        with unittest.mock.patch.dict('os.environ', {}) as _:
            # take no values
            self.assertEqual(file.File.find(), None,
                             "No file is found if none exists. ")

            os_path_isfile.assert_any_call(
                '/path/to/home/.config/.gitmanager/config')
            os_path_isfile.assert_any_call('/path/to/home/.gitmanager')

            # take the first alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [True, False]
            self.assertEqual(file.File.find(),
                             '/path/to/home/.config/.gitmanager/config',
                             "Finding the first file if it exists")

            # take the second alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [False, True]
            self.assertEqual(file.File.find(),
                             '/path/to/home/.gitmanager',
                             "Finding the second file if it exists")

        # reset the mock completly
        os_path_isfile.reset_mock()
        os_path_isfile.side_effect = None
        os_path_isfile.return_value = False

        # only $GIT_MANAGER_CONFIG
        with unittest.mock.patch.dict('os.environ', {
            "GIT_MANAGER_CONFIG": "/path/to/config.file"
        }) as _:
            # take no values
            self.assertEqual(file.File.find(), None,
                             "No file is found if none exists. ")
            os_path_isfile.assert_any_call('/path/to/config.file')
            os_path_isfile.assert_any_call(
                '/path/to/home/.config/.gitmanager/config')
            os_path_isfile.assert_any_call('/path/to/home/.gitmanager')

            # take the first alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [True, False, False]
            self.assertEqual(file.File.find(),
                             '/path/to/config.file',
                             "Finding the first file if it exists")

            # take the second alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [False, True, False]
            self.assertEqual(file.File.find(),
                             '/path/to/home/.config/.gitmanager/config',
                             "Finding the second file if it exists")

            # take the third alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [False, False, True]
            self.assertEqual(file.File.find(),
                             '/path/to/home/.gitmanager',
                             "Finding the third file if it exists")

        os_path_isfile.reset_mock()
        os_path_isfile.side_effect = None
        os_path_isfile.return_value = False

        # only XDG_CONFIG_HOME
        with unittest.mock.patch.dict('os.environ', {
            "XDG_CONFIG_HOME": "/path/to/xdg"
        }) as _:
            # take no values
            self.assertEqual(file.File.find(), None,
                             "No file is found if none exists. ")

            os_path_isfile.assert_any_call(
                '/path/to/xdg/.gitmanager/config')
            os_path_isfile.assert_any_call('/path/to/home/.gitmanager')

            # take the first alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [True, False]
            self.assertEqual(file.File.find(),
                             '/path/to/xdg/.gitmanager/config',
                             "Finding the first file if it exists")

            # take the second alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [False, True]
            self.assertEqual(file.File.find(),
                             '/path/to/home/.gitmanager',
                             "Finding the second file if it exists")

        # reset the mock completely
        os_path_isfile.reset_mock()
        os_path_isfile.side_effect = None
        os_path_isfile.return_value = False

        # both
        with unittest.mock.patch.dict('os.environ', {
            "GIT_MANAGER_CONFIG": "/path/to/config.file",
            "XDG_CONFIG_HOME": "/path/to/xdg"
        }) as _:
            # take no values
            self.assertEqual(file.File.find(), None,
                             "No file is found if none exists. ")
            os_path_isfile.assert_any_call('/path/to/config.file')
            os_path_isfile.assert_any_call(
                '/path/to/xdg/.gitmanager/config')
            os_path_isfile.assert_any_call('/path/to/home/.gitmanager')

            # take the first alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [True, False, False]
            self.assertEqual(file.File.find(),
                             '/path/to/config.file',
                             "Finding the first file if it exists")

            # take the second alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [False, True, False]
            self.assertEqual(file.File.find(),
                             '/path/to/xdg/.gitmanager/config',
                             "Finding the second file if it exists")

            # take the third alternative
            os_path_isfile.reset_mock()
            os_path_isfile.side_effect = [False, False, True]
            self.assertEqual(file.File.find(),
                             '/path/to/home/.gitmanager',
                             "Finding the third file if it exists")
