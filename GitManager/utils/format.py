import shutil
import sys

from os import path


class Format(object):
    """ Methods for formatting text in certain colors. """

    def __init__(self):
        """ Prevents creation of Format(). """
        raise TypeError("Format() can not be instantiated")

    @staticmethod
    def red(prt: str) -> str:
        """ Formats a string in red. """

        return "\033[91m{}\033[00m".format(prt)

    @staticmethod
    def yellow(prt: str) -> str:
        """ Formats a string in yellow. """

        return "\033[93m{}\033[00m".format(prt)

    @staticmethod
    def green(prt: str) -> str:
        """ Formats a string in green. """

        return "\033[92m{}\033[00m".format(prt)

    @staticmethod
    def cyan(prt: str) -> str:
        """ Formats a string in cyan. """

        return "\033[96m{}\033[00m".format(prt)

    @staticmethod
    def short_abs_path(pth: str, length: int) -> str:
        """ Formats an absolute path with a maximum length

        :param pth: Absolute path to format
        :param length: Maximal length of the path (at least 6)
        """

        # too small length
        if length <= 5:
            raise ValueError('Length must be at least 6')

        # check that we have an absolute path
        if not pth.startswith('/'):
            raise ValueError('pth must be an absolute path')

        #
        # Step 1: Normalise the path
        #

        pth = path.normpath(pth)

        if len(pth) < length:
            return pth

        #
        # Step 2: If inside $HOME, use a relative path instead of an
        # absolute one
        #

        # find the path relative to the $HOME directory of the user
        relative_path = path.relpath(pth, path.expanduser('~'))

        # if we are inside the home directory, use that instead
        if relative_path.startswith('./') or relative_path.startswith(
                '../') \
                or relative_path == '.' or relative_path == '..':
            prefix = '/'
            pth = pth[1:]
        else:
            prefix = '~/'
            pth = relative_path

        #
        # Step 3: Format a short path
        #

        return prefix + Format.short_rel_path(pth, length - len(prefix))

    @staticmethod
    def short_rel_path(pth: str, length: int) -> str:
        """ Formats a relative path with a maximum length

        :param pth: Relative path to format
        :param length: Maximal length of the path (at least 4)
        """

        # too small length
        if length <= 3:
            raise ValueError('Length must be at least 4')

        # check that we have a relative path
        if pth.startswith('/'):
            raise ValueError('pth must be a relative path')

        #
        # Step 1: Normalise the path
        #

        pth = path.normpath(pth)

        if len(pth) <= length:
            return pth

        #
        # Step 2: Iteratively try replacing components by '...'
        #

        pth_components = pth.split('/')

        # try shortening components
        while len(pth_components) > 2:

            # if the long path is ok, just return it
            if len(pth) <= length:
                return pth

            # figure out the component to remove
            rmidx = int(len(pth_components) / 2)

            # build a new path
            pth = '/'.join(pth_components[:rmidx] + ['...'] + pth_components[
                                                              (rmidx + 1):])

            # and update the components array
            pth_components = pth_components[:rmidx] + pth_components[
                                                      (rmidx + 1):]

        #
        # Step 3: Fallback to just taking a substring
        #

        # if the long path is ok now, just return it
        if len(pth) <= length:
            return pth

        # if we still haven't gotten a path that is short enough
        # we will have to remove parts from within one component

        # extract first and last component
        begin = pth_components[0]
        end = pth_components[1]

        # the number of characters we will get to keep
        keepidx = length - 3

        # shorten the longer component, as it likely is accurate enough
        # even without the extra information
        if len(begin) < len(end):
            return pth[:keepidx] + '...'
        else:
            return '...' + pth[-keepidx:]

    @staticmethod
    def short_path(pth: str, length: int) -> str:
        """ Formats a path with a maximum length

        If pth is known to be absolute or non-absolute use short_abs_path() or
        short_rel_path() instead.

        :param pth: Path to format
        :param length: Maximal length of the path (at least 6)
        """

        # too small length
        if length <= 5:
            raise ValueError('Length must be at least 6')

        if pth.startswith('/'):
            return Format.short_abs_path(pth, length)
        else:
            return Format.short_rel_path(pth, length)


class TerminalLine(object):
    """ Represents a Terminal Line that can be re-written"""

    def __init__(self, fd=None):
        """ Creates a new TerminalLine object.

        :param fd: File descriptor of output to use
        """

        self.__fd = sys.stdout if fd is None else fd
        self.__cache = ""

    @property
    def width(self):
        """
        :return: the width of this line in number of characters
        :rtype: int
        """

        return shutil.get_terminal_size().columns

    def clean(self):
        """ Cleans the current line of content.

        :return:
        """

        if self.__fd.isatty():
            self.append('\r%s\r' % (' ' * self.width))
        else:
            self.__cache = ""

    def linebreak(self):
        """ Inserts a LineBreak into this line.
        """

        self.append('\n')

    def write(self, s: str):
        """ Writes a string to this Line, overwriting the current content.

        :param s: String to write to the line.
        :type s: str
        """

        self.clean()
        self.append(s)

    def append(self, s: str):
        """ Appends text to this TermminalLine instance. """

        # either write it out directly
        if self.__fd.isatty():
            self.__fd.write(s)
        else:
            self.__cache += s

        # and flush the content
        self.flush()

    def flush(self):
        """Flushes this TerminalLine. """

        # if we are not a terminal, we flush existing lines
        if not self.__fd.isatty():
            while "\n" in self.__cache:
                idx = self.__cache.index('\n')
                self.__fd.write(self.__cache[:idx + 1])
                self.__cache = self.__cache[idx + 1:]

        # call the underlying flush implementation
        self.__fd.flush()


__all__ = ["Format", "TerminalLine"]
