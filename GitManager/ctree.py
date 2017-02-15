import re
import os.path
import typing


class ConfigTree(object):
    """ A single line in the configuration file """

    DIRECTIVE_NOP = re.compile(r'^((\s*)#(.*))|(\s*)$')
    DIRECTIVE_BASE = re.compile(
        r'(\s*)(>+)(\s+)([^\s]+)(?:(\s+)([^\s]+))?(\s*)$')
    DIRECTIVE_REPO = re.compile(r'^(\s*)([^>\s]+)(?:(\s+)([^\s]+))?(\s*)$')

    def __init__(self, indent: str):
        """ Creates a new ConfigTree object

        :param indent: The indent of this ConfigTree Line
        """
        self.__indent = indent

    @property
    def indent(self) -> str:
        return self.__indent

    def write(self) -> str:
        """ Turns this ConfigLine into a string that can be re-parsed """
        raise NotImplementedError

    @staticmethod
    def parse(s: str):
        """ Parses a string into a ConfigLine
        :rtype: ConfigTree"""

        nop_match = ConfigTree.DIRECTIVE_NOP.match(s)
        if nop_match:
            return NOPLine(s)

        base_match = ConfigTree.DIRECTIVE_BASE.match(s)
        if base_match:
            return BaseLine(base_match.group(1), len(base_match.group(2)),
                            base_match.group(3), base_match.group(4),
                            base_match.group(5) or '',
                            base_match.group(6) or '',
                            base_match.group(7))

        repo_match = ConfigTree.DIRECTIVE_REPO.match(s)
        if repo_match:
            return RepoLine(repo_match.group(1), repo_match.group(2),
                            repo_match.group(3) or '',
                            repo_match.group(4) or '',
                            repo_match.group(5))

        raise ValueError("Input does not represent a ConfigLine")


class NOPLine(ConfigTree):
    """ A line without meaning inside the Configuration File """

    def __init__(self, line: str):
        """ Creates a new NopLine instance """
        super().__init__('')

        self.__line = line

    @property
    def content(self) -> str:
        """ The content of this line """
        return self.__line

    def write(self) -> str:
        """ Turns this ConfigLine into a string that can be re-parsed """

        return self.__line

    def __eq__(self, other: typing.Any) -> bool:
        """ Checks that this line is equal to another line """

        return isinstance(other, NOPLine) and self.content == other.content


class BaseLine(ConfigTree):
    """ A line introducing a new BaseLine """

    def __init__(self, indent: str, depth: int, space_1: str, path: str,
                 space_2: str, repo_pat: str, space_3: str):
        """ Creates a new BaseLine instance """

        super().__init__(indent)

        self.__depth = depth
        self.__space_1 = space_1
        self.__path = path
        self.__space_2 = space_2
        self.__repo_pat = repo_pat
        self.__space_3 = space_3

    @property
    def depth(self) -> int:
        """ The depth of this BaseLine directive """
        return self.__depth

    @property
    def path(self) -> str:
        """ The path this BaseLine instance introduces """
        return self.__path

    @property
    def repo_pat(self) -> str:
        """ The repo pattern introduced by this BaseLine """
        return self.__repo_pat

    def write(self) -> str:
        """ Turns this ConfigLine into a string that can be re-parsed """

        return "%s%s%s%s%s%s%s" % (self.indent, ">" * self.depth,
                                   self.__space_1, self.path,
                                   self.__space_2, self.repo_pat,
                                   self.__space_3)

    def __eq__(self, other: typing.Any) -> bool:
        """ Checks that this line is equal to another line """

        return isinstance(other, BaseLine) \
            and self.indent == other.indent\
            and self.depth == other.depth\
            and self.__space_1 == other.__space_1\
            and self.path == other.path\
            and self.__space_2 == other.__space_2\
            and self.repo_pat == other.repo_pat\
            and self.__space_3 == other.__space_3


class RepoLine(ConfigTree):
    """ a line representing a single repository """

    def __init__(self, indent: str, url: str, space_1: str, path: str,
                 space_2: str):
        """ Creates a new RepoLine instance """

        super().__init__(indent)

        self.__url = url
        self.__space_1 = space_1
        self.__path = path
        self.__space_2 = space_2

    @property
    def url(self) -> str:
        """ The url this repo should be cloned from """
        return self.__url

    @property
    def path(self) -> str:
        """ The path this repo should be cloned into """
        return self.__path

    def write(self) -> str:
        """ Turns this ConfigLine into a string that can be re-parsed """

        return "%s%s%s%s%s" % (self.indent, self.url, self.__space_1,
                               self.path, self.__space_2)

    def __eq__(self, other: typing.Any) -> bool:
        """ Checks that this line is equal to another line """

        return isinstance(other, RepoLine) \
            and self.indent == other.indent \
            and self.url == other.url \
            and self.__space_1 == other.__space_1 \
            and self.path == other.path \
            and self.__space_2 == other.__space_2
