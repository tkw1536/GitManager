import unittest

from GitManager.config import line


class TestConfigLine(unittest.TestCase):
    """ Tests that ConfigLines can be correctly parsed"""

    def test_abstract(self):
        """ Tests that the write() method is abstract """

        # because it is abstract, we can not raise it
        with self.assertRaises(NotImplementedError):
            line.ConfigLine.write(None)

    def test_parse_RootLine(self):
        """ Tests that RootLines can be properly parsed """

        self.assertEqual(line.ConfigLine.parse('##root'),
                         line.RootLine('', '', 'root', ''),
                         'parsing root directive')

        self.assertEqual(line.ConfigLine.parse('\t ## /folder '),
                         line.RootLine('\t ', ' ', '/folder', ' '),
                         'parsing comments with tabs')

    def test_parse_NOPLine(self):
        """ Tests that NOPLines can be correctly parsed """

        self.assertEqual(line.ConfigLine.parse('# hello world'),
                         line.NOPLine('# hello world'), 'parsing comments')

        self.assertEqual(line.ConfigLine.parse('# >>> a b'),
                         line.NOPLine('# >>> a b'),
                         'parsing commented out RepoLine')

        self.assertEqual(line.ConfigLine.parse('\t # hello world'),
                         line.NOPLine('\t # hello world'),
                         'parsing comments with spaces')

        self.assertEqual(line.ConfigLine.parse(''), line.NOPLine(''),
                         'parsing empty line')

        self.assertEqual(line.ConfigLine.parse('\t\n  '),
                         line.NOPLine('\t\n  '),
                         'parsing line with only spaces')

    def test_parse_BaseLine(self):
        """ Tests that BaseLines can be correctly parsed """

        self.assertEqual(line.ConfigLine.parse('> hello'),
                         line.BaseLine('', 1, ' ', 'hello', ''),
                         'parsing minimal BaseLine')

        self.assertEqual(line.ConfigLine.parse('>>>> hello'),
                         line.BaseLine('', 4, ' ', 'hello', ''),
                         'parsing minimal BaseLine with more indent')

        self.assertEqual(line.ConfigLine.parse('> hello '),

                         line.BaseLine('', 1, ' ', 'hello', ' '),
                         'parsing complete BaseLine with minimal spacing')

        self.assertEqual(line.ConfigLine.parse('>>>> hello '),
                         line.BaseLine('', 4, ' ', 'hello', ' '),
                         'parsing complete BaseLine with minimal spacing '
                         'and more indent')

        self.assertEqual(line.ConfigLine.parse('\t>>>>\t\thello\t '),
                         line.BaseLine('\t', 4, '\t\t', 'hello', '\t '),
                         'parsing complete BaseLine with spacing '
                         'and more indent')

    def test_parse_RepoLine(self):
        """ Tests that RepoLines can be correctly parsed """

        self.assertEqual(line.ConfigLine.parse('a'),
                         line.RepoLine('', 'a', '', '', ''),
                         'parsing minimal RepoLine')
        self.assertEqual(line.ConfigLine.parse('a b'),
                         line.RepoLine('', 'a', ' ', 'b', ''),
                         'parsing minimal but complete RepoLine')
        self.assertEqual(line.ConfigLine.parse('\ta\t\tb\t\t\t'),
                         line.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t'),
                         'parsing RepoLine with spacing')

    def test_parse_fail(self):
        """ Tests that invalid lines can not be parsed """

        # three items can not be parsed
        with self.assertRaises(ValueError):
            line.ConfigLine.parse("a b c")

        # Comments at the end of the line are not allowed
        with self.assertRaises(ValueError):
            line.ConfigLine.parse("hello world #things")

        with self.assertRaises(ValueError):
            line.ConfigLine.parse(">> hello world #things")


class TestRootLine(unittest.TestCase):
    """ Tests that RootLine class works properly """

    def test_eq(self):
        """ Checks that equality between RootLines works properly """

        self.assertEqual(line.RootLine('', '', '/root', ''),
                         line.RootLine('', '', '/root', ''),
                         'equality of root lines')

        self.assertEqual(line.RootLine('\t ', '', 'folder', ''),
                         line.RootLine('\t ', '', 'folder', ''),
                         'equality of root lines')

    def test_indent(self):
        """ Tests that the indent function works properly  """
        self.assertEqual(line.RootLine('\t ', '', 'folder', '').indent,
                         '\t ', 'indent of root line')

        self.assertEqual(line.RootLine('', '', '/root', '').indent,
                         '', 'indent of root line')

    def test_write(self):
        """ Tests that writing NOPLines works properly """
        self.assertEqual(line.RootLine('', '', '/root', '').write(),
                         '##/root', 'writing root line')

        self.assertEqual(line.RootLine('\t ', '', 'folder', '').write(),
                         '\t ##folder', 'writing root line')

    def test_root(self):
        """ Tests that the root attribute is read correctly """
        self.assertEqual(line.RootLine('', '', '/root', '').root,
                         '/root', 'root of root line')

        self.assertEqual(line.RootLine('\t ', '', 'folder', '').root,
                         'folder', 'root of root line')


class TestNOPLine(unittest.TestCase):
    """ Tests that NOPLine class works properly """

    def test_eq(self):
        """ Checks that equality between NOPLines works properly """

        self.assertEqual(line.NOPLine('# hello world'),
                         line.NOPLine('# hello world'),
                         'equality of comments')

        self.assertEqual(line.NOPLine('# >>> a b'),
                         line.NOPLine('# >>> a b'),
                         'equality of commented out RepoLines')

        self.assertEqual(line.NOPLine('\t # hello world'),
                         line.NOPLine('\t # hello world'),
                         'equality comments with spaces')

        self.assertEqual(line.NOPLine(''), line.NOPLine(''),
                         'equality of empty lines')

        self.assertEqual(line.NOPLine('\t\n  '),
                         line.NOPLine('\t\n  '),
                         'equality of lines with only spaces')

        self.assertNotEqual(line.NOPLine('\t\n  '),
                            line.NOPLine('\t\n '),
                            'inequality of two different NOPLines')

        self.assertNotEqual(line.NOPLine('\t\n  '),
                            line.ConfigLine(''),
                            'inequality between two different objects')

    def test_indent(self):
        """ Tests that the indent function works properly  """
        self.assertEqual(line.NOPLine('# hello world').indent,
                         '', 'indent of comment line')

        self.assertEqual(line.NOPLine('# >>> a b').indent,
                         '', 'content of commented out RepoLine')

        self.assertEqual(line.NOPLine('\t # hello world').indent,
                         '',
                         'indent of comments with spaces')

        self.assertEqual(line.NOPLine('').indent, '',
                         'indent of empty line')

        self.assertEqual(line.NOPLine('\t\n  ').indent, '',
                         'indent of line with only spaces')

    def test_write(self):
        """ Tests that writing NOPLines works properly """
        self.assertEqual(line.NOPLine('# hello world').write(),
                         '# hello world', 'writing comment line')

        self.assertEqual(line.NOPLine('# >>> a b').write(),
                         '# >>> a b', 'writing commented out RepoLine')

        self.assertEqual(line.NOPLine('\t # hello world').write(),
                         '\t # hello world',
                         'writing comments with spaces')

        self.assertEqual(line.NOPLine('').write(), '', 'writing empty line')

        self.assertEqual(line.NOPLine('\t\n  ').write(), '\t\n  ',
                         'writing line with only spaces')

    def test_content(self):
        """ Tests that the content attribute is read correctly """
        self.assertEqual(line.NOPLine('# hello world').content,
                         '# hello world', 'content of comment line')

        self.assertEqual(line.NOPLine('# >>> a b').content,
                         '# >>> a b', 'content of commented out RepoLine')

        self.assertEqual(line.NOPLine('\t # hello world').content,
                         '\t # hello world',
                         'content of comments with spaces')

        self.assertEqual(line.NOPLine('').content, '',
                         'content of empty line')

        self.assertEqual(line.NOPLine('\t\n  ').content, '\t\n  ',
                         'content of line with only spaces')


class TestBaseLine(unittest.TestCase):
    """ Tests that BaseLine class works properly """

    def test_eq(self):
        """ Tests that equality between BaseLines works properly """

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', ''),
                         line.BaseLine('', 1, ' ', 'hello', ''),
                         'equality between minimal BaseLines')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', ''),
                         line.BaseLine('', 4, ' ', 'hello', ''),
                         'equality between minimal BaseLines with more indent')

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', ' '),
                         line.BaseLine('', 1, ' ', 'hello', ' '),
                         'equality between complete BaseLines with minimal '
                         'spacing')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', ' '),
                         line.BaseLine('', 4, ' ', 'hello', ' '),
                         'equality between complete BaseLines with minimal '
                         'spacing and more indent')

        self.assertEqual(line.BaseLine('\t', 4, '\t\t', 'hello', '\t '),
                         line.BaseLine('\t', 4, '\t\t', 'hello', '\t '),
                         'equality between complete BaseLines with spacing '
                         'and more indent')

        self.assertNotEqual(line.BaseLine('', 1, ' ', 'hello', ''),
                            line.BaseLine('', 4, ' ', 'hello', ''),
                            'inequality between different BaseLines')

        self.assertNotEqual(line.BaseLine('', 1, ' ', 'hello', ''),
                            line.ConfigLine(''),
                            'inequality between BaseLine and instance of '
                            'other class')

    def test_indent(self):
        """ Tests that the indent function works properly  """
        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', '').indent,
                         '',
                         'indent of minimal BaseLine')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', '').indent,
                         '',
                         'indent of minimal BaseLines with more '
                         'indent')

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', ' ').indent,
                         '',
                         'indent of complete BaseLine with minimal spacing')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', ' ').indent,
                         '',
                         'indent of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(line.BaseLine('\t', 4, '\t\t', 'hello', '\t ').indent,
                         '\t',
                         'indent of complete BaseLines with spacing '
                         'and more indent')

    def test_write(self):
        """ Tests that writing BaseLines works properly """

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', '').write(),
                         '> hello', 'writing minimal BaseLine')

        self.assertEqual(
            line.BaseLine('', 4, ' ', 'hello', '').write(),
            '>>>> hello',
            'writing minimal BaseLine with more indent')

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', ' ').write(),
                         '> hello ',
                         'writing complete BaseLine with minimal spacing')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', ' ').write(),
                         '>>>> hello ',
                         'writing complete BaseLine with minimal spacing '
                         'and more indent')

        self.assertEqual(
            line.BaseLine('\t', 4, '\t\t', 'hello', '\t ').write(),
            '\t>>>>\t\thello\t ',
            'writing complete BaseLine with spacing '
            'and more indent')

    def test_depth(self):
        """ Tests that the depth property is read correctly """
        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', '').depth,
                         1, 'reading depth of minimal BaseLine')

        self.assertEqual(
            line.BaseLine('', 4, ' ', 'hello', '').depth,
            4,
            'reading depth of minimal BaseLine with more indent')

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', ' ').depth,
                         1,
                         'reading depth of complete BaseLine with minimal '
                         'spacing')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', ' ').depth,
                         4,
                         'reading depth of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(line.BaseLine('\t', 4, '\t\t', 'hello', '\t ').depth,
                         4,
                         'reading depth of complete BaseLine with spacing '
                         'and more indent')

    def test_path(self):
        """ Tests that the path property is read correctly """
        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', '').path,
                         'hello', 'reading path of minimal BaseLine')

        self.assertEqual(
            line.BaseLine('', 4, ' ', 'hello', '').path,
            'hello',
            'reading path of minimal BaseLine with more indent')

        self.assertEqual(line.BaseLine('', 1, ' ', 'hello', ' ').path,
                         'hello',
                         'reading path of complete BaseLine with minimal '
                         'spacing')

        self.assertEqual(line.BaseLine('', 4, ' ', 'hello', ' ').path,
                         'hello',
                         'reading path of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(line.BaseLine('\t', 4, '\t\t', 'hello', '\t ').path,
                         'hello',
                         'reading path of complete BaseLine with spacing '
                         'and more indent')


class TestRepoLine(unittest.TestCase):
    """ Tests that RepoLine class works properly """

    def test_eq(self):
        """ Tests that equality between repo lines works properly """

        self.assertEqual(line.RepoLine('', 'a', '', '', ''),
                         line.RepoLine('', 'a', '', '', ''),
                         'equality between minimal RepoLines')
        self.assertEqual(line.RepoLine('', 'a', ' ', 'b', ''),
                         line.RepoLine('', 'a', ' ', 'b', ''),
                         'equality between minimal but complete RepoLines')
        self.assertEqual(line.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t'),
                         line.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t'),
                         'equality RepoLines with spacing')

        self.assertNotEqual(line.RepoLine('', 'a', '', '', ''),
                            line.RepoLine('  ', 'a', '', '', ''),
                            'inequality between different RepoLines')

        self.assertNotEqual(line.RepoLine('', 'a', '', '', ''),
                            line.ConfigLine(' '),
                            'inequality between RepoLine and instance of a '
                            'different class')

    def test_indent(self):
        """ Tests that the indent function works properly  """

        self.assertEqual(line.RepoLine('', 'a', '', '', '').indent,
                         '',
                         'indent of minimal RepoLine')
        self.assertEqual(line.RepoLine('', 'a', ' ', 'b', '').indent,
                         '',
                         'indent of minimal but complete RepoLine')
        self.assertEqual(line.RepoLine('\t', 'a', '\t\t', 'b',
                                       '\t\t\t').indent,
                         '\t',
                         'indent of RepoLine with spacing')

    def test_write(self):
        """ Tests that writing RepoLines works properly """

        self.assertEqual(line.RepoLine('', 'a', '', '', '').write(),
                         'a',
                         'writing minimal RepoLine')

        self.assertEqual(line.RepoLine('', 'a', ' ', 'b', '').write(),
                         'a b',
                         'writing minimal but complete RepoLine')

        self.assertEqual(
            line.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t').write(),
            '\ta\t\tb\t\t\t',
            'writing RepoLine with spacing')

    def test_url(self):
        """ Tests that the url property is read properly """

        self.assertEqual(line.RepoLine('', 'a', '', '', '').url,
                         'a',
                         'getting url of minimal RepoLine')

        self.assertEqual(line.RepoLine('', 'a', ' ', 'b', '').url,
                         'a',
                         'getting url of minimal but complete RepoLine')

        self.assertEqual(
            line.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t').url,
            'a',
            'getting url of RepoLine with spacing')

    def test_path(self):
        """ Tests that the path property is read properly """

        self.assertEqual(line.RepoLine('', 'a', '', '', '').path,
                         '',
                         'getting path of minimal RepoLine')

        self.assertEqual(line.RepoLine('', 'a', ' ', 'b', '').path,
                         'b',
                         'getting path of minimal but complete RepoLine')

        self.assertEqual(
            line.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t').path,
            'b',
            'getting path of RepoLine with spacing')
