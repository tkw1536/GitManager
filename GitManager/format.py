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

__all__ = ["Format"]
