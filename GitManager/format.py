import shutil
import sys

from os import path

class Format(object):
    """ Methods for formatting text in certain colors. """

    def __init__(self):
        """ Prevents creation of Format(). """
        raise TypeError("Format() can not be instantiated")

    @staticmethod
    def red(prt):
        """ Formats a string in red. """

        return "\033[91m{}\033[00m".format(prt)

    @staticmethod
    def yellow(prt):
        """ Formats a string in yellow. """

        return "\033[93m{}\033[00m".format(prt)

    @staticmethod
    def green(prt):
        """ Formats a string in green. """

        return "\033[92m{}\033[00m".format(prt)

    @staticmethod
    def cyan(prt):
        """ Formats a string in cyan. """

        return "\033[96m{}\033[00m".format(prt)

    @staticmethod
    def path(pth, l):
        """ Formats a local path in a human readable way.

        :param path: Path to format
        :type path: str

        :param l: Length to format path with.
        :type l: Maximal length of the path
        """

        # Try to make a relative path to $HOME
        rhome = path.relpath(pth, path.expanduser('~'))

        # Check if it is a relative path
        is_home_relative = rhome.startswith('./') or rhome.startswith('../') or rhome == '.' or rhome=='..'

        if is_home_relative:
            long_path = pth
        else:
            long_path = path.join('~', rhome)

        # split into components
        path_components = long_path.split('/')

        # try shortening components
        while len(path_components) > 2:

            # if the long path is ok, just return it
            if len(long_path) <= l:
                return long_path

            # figure out the component to remove
            rmidx = int(len(path_components) / 2)

            # build a new path
            long_path = '/'.join(path_components[:rmidx] + ['...'] + path_components[(rmidx+1):])

            # and update the components array
            path_components = path_components[:rmidx] + path_components[(rmidx+1):]

        # if we still haven't gotten a path that is short enough
        # we will have to remove parts from within one component

        # extract first and last component
        begin = path_components[0]
        end = path_components[1]

        # the number of characters we will get to keep
        keepidx = l - 3

        # shorten one of the components, whichever is shorter
        if len(begin) < len(end):
            return '...' + begin[-keepidx:]
        else:
            return end[:keepidx] + '...'

class TerminalLine(object):
    """ Represents a Terminal Line that can be re-written"""
    def __init__(self):
        """
        Creates a new TerminalLine object.
        """

        self.__fd = sys.__stdout__

    @property
    def width(self):
        """
        :return: the width of this line in number of characters or -1.
        :rtype: int
        """


        try:
            return shutil.get_terminal_size().columns
        except OSError:
            return -1

    def clean(self):
        """ Cleans the current line of content.

        :return:
        """

        self.append('\r%s\r' % (' '* self.width))

    def write(self, s):
        """ Writes a string to this Line, overwriting the current content.

        :param s: String to write to the line.
        :type s: str
        """

        self.clean()
        self.append(s)

    def append(self, s):
        """ Appends text to this TermminalLine instance. """

        self.__fd.write(s)
        self.__fd.flush()




__all__ = ["Format"]
