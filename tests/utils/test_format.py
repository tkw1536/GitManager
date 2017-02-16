import unittest
import unittest.mock

from GitManager.utils import format


class TestFormat(unittest.TestCase):
    """ Tests that the Format() class works properly """

    def test_init(self):
        """ Tests that format can not be instantiated """

        with self.assertRaises(TypeError):
            format.Format()

    def test_red(self):
        """ Tests that the red method works properly """

        self.assertEqual(format.Format.red("Hello"), "\033[91mHello\033[00m")

    def test_yellow(self):
        """ Tests that the yelloe method works properly """

        self.assertEqual(format.Format.yellow("Hello"),
                         "\033[93mHello\033[00m")

    def test_green(self):
        """ Tests that the green method works properly """

        self.assertEqual(format.Format.green("Hello"), "\033[92mHello\033[00m")

    def test_cyan(self):
        """ Tests that the cyan method works properly """

        self.assertEqual(format.Format.cyan("Hello"), "\033[96mHello\033[00m")

    @unittest.mock.patch.object(format.Format, 'short_rel_path')
    @unittest.mock.patch('os.path.expanduser', return_value='/home/user')
    def test_short_abs_path(self,
                            os_path_expanduser: unittest.mock.Mock,
                            format_short_rel_path: unittest.mock.Mock):
        # length is too short
        with self.assertRaises(ValueError):
            format.Format.short_abs_path('hello/world', 3)

        # must be an absolute path
        with self.assertRaises(ValueError):
            format.Format.short_abs_path('hello/world', 10)

        # short path outside of $HOME
        self.assertEqual(
            format.Format.short_abs_path('/hello/world', 15),
            '/hello/world', 'short path outside of $HOME is left as is'
        )

        format_short_rel_path.assert_not_called()
        format_short_rel_path.reset_mock()

        # short path inside of $HOME
        self.assertEqual(
            format.Format.short_abs_path('/home/user/hello/world', 100),
            '/home/user/hello/world',
            'short path inside of $HOME is left as is'
        )

        format_short_rel_path.assert_not_called()
        format_short_rel_path.reset_mock()

        # path to be shortened outside of $HOME
        format_short_rel_path.return_value = 'hello/.../world'

        self.assertEqual(
            format.Format.short_abs_path('/hello/brave/world', 16),
            '/hello/.../world', 'path to be shortened outside of $HOME'
        )

        format_short_rel_path.assert_called_with('hello/brave/world', 15)
        format_short_rel_path.reset_mock()

        # path to be shortened inside of $HOME
        format_short_rel_path.return_value = 'hello/.../world'

        self.assertEqual(
            format.Format.short_abs_path('/home/user/hello/brave/world', 17),
            '~/hello/.../world', 'path to be shortened inside of $HOME'
        )

        format_short_rel_path.assert_called_with('hello/brave/world', 15)
        format_short_rel_path.reset_mock()

    def test_short_rel_path(self):
        """ Tests that the short_rel_path() method works properly """

        # length is too short
        with self.assertRaises(ValueError):
            format.Format.short_rel_path('hello/world', 2)

        # must be a relative path
        with self.assertRaises(ValueError):
            format.Format.short_rel_path('/hello/world', 10)

        self.assertEqual(format.Format.short_rel_path('hello/world', 15),
                         'hello/world', 'short path is given as is')

        self.assertEqual(
            format.Format.short_rel_path('hello/a/b//../.././/world', 15),
            'hello/world', 'convoluted path is cleaned up automatically')

        self.assertEqual(
            format.Format.short_rel_path('hello/brave/world', 15),
            'hello/.../world', 'replacing middle of three-component path '
                               'properly'
        )

        self.assertEqual(
            format.Format.short_rel_path('1234567890/1234/', 15),
            '1234567890/1234', 'remove unneeded slash from the end')

        self.assertEqual(
            format.Format.short_rel_path('a/b/cc/ddd/eeeee', 15),
            'a/b/.../eeeee', 'replacing long path properly'
        )

        self.assertEqual(
            format.Format.short_rel_path('hello/oh/brave/new/world', 15),
            'hello/.../world', 'replacing long path properly'
        )

        self.assertEqual(
            format.Format.short_rel_path('aaaaaaaaaa/bbbbb', 15),
            '...aaaaaa/bbbbb', 'shorten path from the start'
        )

        self.assertEqual(
            format.Format.short_rel_path('bbbbb/aaaaaaaaaa', 15),
            'bbbbb/aaaaaa...', 'shorten path from the start'
        )

    @unittest.mock.patch.object(format.Format, 'short_rel_path',
                                return_value='hello/world')
    @unittest.mock.patch.object(format.Format, 'short_abs_path',
                                return_value='/hello/world')
    def test_rel_path(self,
                      format_short_abs_path: unittest.mock.Mock,
                      format_short_rel_path: unittest.mock.Mock):
        """ Tests that the short_path() method works properly """

        # length is too short
        with self.assertRaises(ValueError):
            format.Format.short_path('hello/world', 5)

        # format absolute path

        self.assertEqual(format.Format.short_path('/hello/world', 15),
                         '/hello/world', 'shorten absolute path')

        format_short_abs_path.assert_called_with('/hello/world', 15)
        format_short_abs_path.reset_mock()

        format_short_rel_path.assert_not_called()
        format_short_rel_path.reset_mock()

        # format relative path
        self.assertEqual(format.Format.short_path('hello/world', 15),
                         'hello/world', 'shorten relative path')

        format_short_rel_path.assert_called_with('hello/world', 15)
        format_short_rel_path.reset_mock()

        format_short_abs_path.assert_not_called()
        format_short_abs_path.reset_mock()


class TestTerminalLine(unittest.TestCase):
    """ Tests that the TerminalLine() class works properly"""

    @unittest.mock.patch('shutil.get_terminal_size')
    def test_width(self, shutil_get_terminal_size: unittest.mock.Mock):
        """ Tests that format.width works properly """

        shutil_get_terminal_size.return_value.columns = 20

        self.assertEqual(format.TerminalLine().width, 20, "width of a "
                                                          "TerminalLine")
        shutil_get_terminal_size.assert_called_with()

    @unittest.mock.patch.object(format.TerminalLine, 'width', 20)
    @unittest.mock.patch.object(format.TerminalLine, 'append')
    @unittest.mock.patch('sys.stdout.isatty')
    def test_clean(self,
                   sys_stdout_isatty: unittest.mock.Mock,
                   format_terminal_line_append: unittest.mock.Mock):
        """ Tests that format.clean works properly """

        # resetting on a tty
        sys_stdout_isatty.return_value = True
        format.TerminalLine().clean()
        format_terminal_line_append.assert_called_with(
            '\r                    \r')

        # resetting on a non tty
        sys_stdout_isatty.return_value = False
        format.TerminalLine().clean()
        format_terminal_line_append.assert_called_with(
            '\n')

    @unittest.mock.patch.object(format.TerminalLine, 'append')
    def test_linebreak(self,
                       format_terminal_line_append: unittest.mock.Mock):
        """ Tests that format.linebreak works correctly"""

        tl = format.TerminalLine()
        tl.linebreak()

        format_terminal_line_append.assert_called_with(
            '\n')

    @unittest.mock.patch.object(format.TerminalLine, 'clean')
    @unittest.mock.patch.object(format.TerminalLine, 'append')
    def test_write(self,
                   format_terminal_line_append: unittest.mock.Mock,
                   format_terminal_line_clean: unittest.mock.Mock):
        """ Tests that format.clean works properly """

        format.TerminalLine().write('Hello world')

        format_terminal_line_clean.assert_called_with()
        format_terminal_line_append.assert_called_with('Hello world')

    @unittest.mock.patch('sys.stdout')
    def test_append(self,
                    sys_stdout: unittest.mock.Mock):
        """ Tests that format.clean works properly """

        tl = format.TerminalLine()
        tl.append('Hello world')

        sys_stdout.write.assert_called_with('Hello world')
        sys_stdout.flush.assert_called_with()
