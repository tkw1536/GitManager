import unittest

from GitManager import ctree


class TestConfigTree(unittest.TestCase):
    """ Tests that LocalVaultLines can be correctly parsed"""

    def test_abstract(self):
        """ Tests that the write() method is abstract """

        # because it is abstract, we can not raise it
        with self.assertRaises(NotImplementedError):
            ctree.ConfigTree.write(None)

    def test_parse_NOPLine(self):
        """ Tests that NOPLines can be correctly parsed """

        self.assertEqual(ctree.ConfigTree.parse('# hello world'),
                         ctree.NOPLine('# hello world'), 'parsing comments')

        self.assertEqual(ctree.ConfigTree.parse('# >>> a b'),
                         ctree.NOPLine('# >>> a b'),
                         'parsing commented out RepoLine')

        self.assertEqual(ctree.ConfigTree.parse('\t # hello world'),
                         ctree.NOPLine('\t # hello world'),
                         'parsing comments with spaces')

        self.assertEqual(ctree.ConfigTree.parse(''), ctree.NOPLine(''),
                         'parsing empty line')

        self.assertEqual(ctree.ConfigTree.parse('\t\n  '),
                         ctree.NOPLine('\t\n  '),
                         'parsing line with only spaces')

    def test_parse_BaseLine(self):
        """ Tests that BaseLines can be correctly parsed """

        self.assertEqual(ctree.ConfigTree.parse('> hello'),
                         ctree.BaseLine('', 1, ' ', 'hello', '', '', ''),
                         'parsing minimal BaseLine')

        self.assertEqual(ctree.ConfigTree.parse('>>>> hello'),
                         ctree.BaseLine('', 4, ' ', 'hello', '', '', ''),
                         'parsing minimal BaseLine with more indent')

        self.assertEqual(ctree.ConfigTree.parse('> hello world'),
                         ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world', ''),
                         'parsing complete BaseLine with minimal spacing')

        self.assertEqual(ctree.ConfigTree.parse('>>>> hello world'),
                         ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world', ''),
                         'parsing complete BaseLine with minimal spacing '
                         'and more indent')

        self.assertEqual(ctree.ConfigTree.parse('\t>>>>\t\thello\t '
                                                'world\t'),
                         ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t'),
                         'parsing complete BaseLine with spacing '
                         'and more indent')

    def test_parse_RepoLine(self):
        """ Tests that RepoLines can be correctly parsed """

        self.assertEqual(ctree.ConfigTree.parse('a'),
                         ctree.RepoLine('', 'a', '', '', ''),
                         'parsing minimal RepoLine')
        self.assertEqual(ctree.ConfigTree.parse('a b'),
                         ctree.RepoLine('', 'a', ' ', 'b', ''),
                         'parsing minimal but complete RepoLine')
        self.assertEqual(ctree.ConfigTree.parse('\ta\t\tb\t\t\t'),
                         ctree.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t'),
                         'parsing RepoLine with spacing')

    def test_parse_fail(self):
        """ Tests that invalid lines can not be parsed """

        # three items can not be parsed
        with self.assertRaises(ValueError):
            ctree.ConfigTree.parse("a b c")

        # Comments at the end of the line are not allowed
        with self.assertRaises(ValueError):
            ctree.ConfigTree.parse("hello world #things")

        with self.assertRaises(ValueError):
            ctree.ConfigTree.parse(">> hello world #things")


class TestNOPLine(unittest.TestCase):
    """ Tests that NOPLine class works properly """

    def test_eq(self):
        """ Checks that equality between NOPLines works properly """

        self.assertEqual(ctree.NOPLine('# hello world'),
                         ctree.NOPLine('# hello world'),
                         'equality of comments')

        self.assertEqual(ctree.NOPLine('# >>> a b'),
                         ctree.NOPLine('# >>> a b'),
                         'equality of commented out RepoLines')

        self.assertEqual(ctree.NOPLine('\t # hello world'),
                         ctree.NOPLine('\t # hello world'),
                         'equality comments with spaces')

        self.assertEqual(ctree.NOPLine(''), ctree.NOPLine(''),
                         'equality of empty lines')

        self.assertEqual(ctree.NOPLine('\t\n  '),
                         ctree.NOPLine('\t\n  '),
                         'equality of lines with only spaces')

        self.assertNotEqual(ctree.NOPLine('\t\n  '),
                            ctree.NOPLine('\t\n '),
                            'inequality of two different NOPLines')

        self.assertNotEqual(ctree.NOPLine('\t\n  '),
                            ctree.ConfigTree(''),
                            'inequality between two different objects')

    def test_indent(self):
        """ Tests that the indent function works properly  """
        self.assertEqual(ctree.NOPLine('# hello world').indent,
                         '', 'indent of comment line')

        self.assertEqual(ctree.NOPLine('# >>> a b').indent,
                         '', 'content of commented out RepoLine')

        self.assertEqual(ctree.NOPLine('\t # hello world').indent,
                         '',
                         'indent of comments with spaces')

        self.assertEqual(ctree.NOPLine('').indent, '',
                         'indent of empty line')

        self.assertEqual(ctree.NOPLine('\t\n  ').indent, '',
                         'indent of line with only spaces')

    def test_write(self):
        """ Tests that writing NOPLines works properly """
        self.assertEqual(ctree.NOPLine('# hello world').write(),
                         '# hello world', 'writing comment line')

        self.assertEqual(ctree.NOPLine('# >>> a b').write(),
                         '# >>> a b', 'writing commented out RepoLine')

        self.assertEqual(ctree.NOPLine('\t # hello world').write(),
                         '\t # hello world',
                         'writing comments with spaces')

        self.assertEqual(ctree.NOPLine('').write(), '', 'writing empty line')

        self.assertEqual(ctree.NOPLine('\t\n  ').write(), '\t\n  ',
                         'writing line with only spaces')

    def test_content(self):
        """ Tests that the content attribute is read correctly """
        self.assertEqual(ctree.NOPLine('# hello world').content,
                         '# hello world', 'content of comment line')

        self.assertEqual(ctree.NOPLine('# >>> a b').content,
                         '# >>> a b', 'content of commented out RepoLine')

        self.assertEqual(ctree.NOPLine('\t # hello world').content,
                         '\t # hello world',
                         'content of comments with spaces')

        self.assertEqual(ctree.NOPLine('').content, '',
                         'content of empty line')

        self.assertEqual(ctree.NOPLine('\t\n  ').content, '\t\n  ',
                         'content of line with only spaces')


class TestBaseLine(unittest.TestCase):
    """ Tests that BaseLine class works properly """

    def test_eq(self):
        """ Tests that equality between BaseLines works properly """

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '', ''),
                         ctree.BaseLine('', 1, ' ', 'hello', '', '', ''),
                         'equality between minimal BaseLines')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', '', '', ''),
                         ctree.BaseLine('', 4, ' ', 'hello', '', '', ''),
                         'equality between minimal BaseLines with more indent')

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world', ''),
                         ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world', ''),
                         'equality between complete BaseLines with minimal '
                         'spacing')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world', ''),
                         ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world', ''),
                         'equality between complete BaseLines with minimal '
                         'spacing and more indent')

        self.assertEqual(ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t'),
                         ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t'),
                         'equality between complete BaseLines with spacing '
                         'and more indent')

        self.assertNotEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '', ''),
                            ctree.BaseLine('', 4, ' ', 'hello', '', '', ''),
                            'inequality between different BaseLines')

        self.assertNotEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '', ''),
                            ctree.ConfigTree(''),
                            'inequality between BaseLine and instance of '
                            'other class')

    def test_indent(self):
        """ Tests that the indent function works properly  """
        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '',
                                        '').indent,
                         '',
                         'indent of minimal BaseLine')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', '', '',
                                        '').indent,
                         '',
                         'indent of minimal BaseLines with more '
                         'indent')

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world',
                                        '').indent,
                         '',
                         'indent of complete BaseLine with minimal spacing')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world',
                                        '').indent,
                         '',
                         'indent of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t').indent,
                         '\t',
                         'indent of complete BaseLines with spacing '
                         'and more indent')

    def test_write(self):
        """ Tests that writing BaseLines works properly """

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '',
                                        '').write(),
                         '> hello', 'writing minimal BaseLine')

        self.assertEqual(
            ctree.BaseLine('', 4, ' ', 'hello', '', '', '').write(),
            '>>>> hello',
            'writing minimal BaseLine with more indent')

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world',
                                        '').write(),
                         '> hello world',
                         'writing complete BaseLine with minimal spacing')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world',
                                        '').write(),
                         '>>>> hello world',
                         'writing complete BaseLine with minimal spacing '
                         'and more indent')

        self.assertEqual(ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t').write(),
                         '\t>>>>\t\thello\t world\t',
                         'writing complete BaseLine with spacing '
                         'and more indent')

    def test_depth(self):
        """ Tests that the depth property is read correctly """
        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '',
                                        '').depth,
                         1, 'reading depth of minimal BaseLine')

        self.assertEqual(
            ctree.BaseLine('', 4, ' ', 'hello', '', '', '').depth,
            4,
            'reading depth of minimal BaseLine with more indent')

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world',
                                        '').depth,
                         1,
                         'reading depth of complete BaseLine with minimal '
                         'spacing')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world',
                                        '').depth,
                         4,
                         'reading depth of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t').depth,
                         4,
                         'reading depth of complete BaseLine with spacing '
                         'and more indent')

    def test_path(self):
        """ Tests that the path property is read correctly """
        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '',
                                        '').path,
                         'hello', 'reading path of minimal BaseLine')

        self.assertEqual(
            ctree.BaseLine('', 4, ' ', 'hello', '', '', '').path,
            'hello',
            'reading path of minimal BaseLine with more indent')

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world',
                                        '').path,
                         'hello',
                         'reading path of complete BaseLine with minimal '
                         'spacing')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world',
                                        '').path,
                         'hello',
                         'reading path of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t').path,
                         'hello',
                         'reading path of complete BaseLine with spacing '
                         'and more indent')

    def test_repo_pat(self):
        """ Tests that the repo_pat property is read correctly """
        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', '', '',
                                        '').repo_pat,
                         '', 'reading repo_pat of minimal BaseLine')

        self.assertEqual(
            ctree.BaseLine('', 4, ' ', 'hello', '', '', '').repo_pat,
            '',
            'reading repo_pat of minimal BaseLine with more indent')

        self.assertEqual(ctree.BaseLine('', 1, ' ', 'hello', ' ', 'world',
                                        '').repo_pat,
                         'world',
                         'reading repo_pat of complete BaseLine with minimal '
                         'spacing')

        self.assertEqual(ctree.BaseLine('', 4, ' ', 'hello', ' ', 'world',
                                        '').repo_pat,
                         'world',
                         'reading repo_pat of complete BaseLine with minimal '
                         'spacing and more indent')

        self.assertEqual(ctree.BaseLine('\t', 4, '\t\t', 'hello', '\t ',
                                        'world', '\t').repo_pat,
                         'world',
                         'reading repo_pat of complete BaseLine with spacing '
                         'and more indent')


class TestRepoLine(unittest.TestCase):
    """ Tests that RepoLine class works properly """

    def test_eq(self):
        """ Tests that equality between repo lines works properly """

        self.assertEqual(ctree.RepoLine('', 'a', '', '', ''),
                         ctree.RepoLine('', 'a', '', '', ''),
                         'equality between minimal RepoLines')
        self.assertEqual(ctree.RepoLine('', 'a', ' ', 'b', ''),
                         ctree.RepoLine('', 'a', ' ', 'b', ''),
                         'equality between minimal but complete RepoLines')
        self.assertEqual(ctree.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t'),
                         ctree.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t'),
                         'equality RepoLines with spacing')

        self.assertNotEqual(ctree.RepoLine('', 'a', '', '', ''),
                            ctree.RepoLine('  ', 'a', '', '', ''),
                            'inequality between different RepoLines')

        self.assertNotEqual(ctree.RepoLine('', 'a', '', '', ''),
                            ctree.ConfigTree(' '),
                            'inequality between RepoLine and instance of a '
                            'different class')

    def test_indent(self):
        """ Tests that the indent function works properly  """

        self.assertEqual(ctree.RepoLine('', 'a', '', '', '').indent,
                         '',
                         'indent of minimal RepoLine')
        self.assertEqual(ctree.RepoLine('', 'a', ' ', 'b', '').indent,
                         '',
                         'indent of minimal but complete RepoLine')
        self.assertEqual(ctree.RepoLine('\t', 'a', '\t\t', 'b',
                                        '\t\t\t').indent,
                         '\t',
                         'indent of RepoLine with spacing')

    def test_write(self):
        """ Tests that writing RepoLines works properly """

        self.assertEqual(ctree.RepoLine('', 'a', '', '', '').write(),
                         'a',
                         'writing minimal RepoLine')

        self.assertEqual(ctree.RepoLine('', 'a', ' ', 'b', '').write(),
                         'a b',
                         'writing minimal but complete RepoLine')

        self.assertEqual(
            ctree.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t').write(),
            '\ta\t\tb\t\t\t',
            'writing RepoLine with spacing')

    def test_url(self):
        """ Tests that the url property is read properly """

        self.assertEqual(ctree.RepoLine('', 'a', '', '', '').url,
                         'a',
                         'getting url of minimal RepoLine')

        self.assertEqual(ctree.RepoLine('', 'a', ' ', 'b', '').url,
                         'a',
                         'getting url of minimal but complete RepoLine')

        self.assertEqual(
            ctree.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t').url,
            'a',
            'getting url of RepoLine with spacing')

    def test_path(self):
        """ Tests that the path property is read properly """

        self.assertEqual(ctree.RepoLine('', 'a', '', '', '').path,
                         '',
                         'getting path of minimal RepoLine')

        self.assertEqual(ctree.RepoLine('', 'a', ' ', 'b', '').path,
                         'b',
                         'getting path of minimal but complete RepoLine')

        self.assertEqual(
            ctree.RepoLine('\t', 'a', '\t\t', 'b', '\t\t\t').path,
            'b',
            'getting path of RepoLine with spacing')
