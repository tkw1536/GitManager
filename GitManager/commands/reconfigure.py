import typing
import argparse

from ..config import file
from ..repo import finder
from ..utils import format

import os
import sys


class Reconfigure(object):
    """ Reconfigure the configuration file"""

    def __init__(self, line: format.TerminalLine, f: file.File, *args: str):
        self.file = f
        self.line = line
        self.args = self.parse(*args)

    def parse(self, *args: str) -> typing.Any:
        """ Parses arguments given to this Command """

        parser = argparse.ArgumentParser(prog='git-manager reconfigure',
                                         description='Recursively add '
                                                     'repositories to the '
                                                     'configuration file')

        parser.add_argument('--simulate', '-s', dest='simulate',
                            action='store_true', default=False,
                            help='Instead of writing out the configuration '
                                 'file to disk, print it to STDOUT. ')

        parser.add_argument('--rebuild', '-r', dest='rebuild',
                            action='store_true', default=False,
                            help='Rebuild and clean up the configuration '
                                 'file, removing empty groups. ')

        parser.add_argument('--clear', '-c', dest='clear',
                            action='store_true', default=False,
                            help='Clear all existing repositories from the '
                                 'configuration. ')

        parser.add_argument('--follow-symlinks', '-f', dest='follow_symlinks',
                            action='store_true', default=False,
                            help='When looking for repositories to add, '
                                 'automatically follow symlinks. Use with '
                                 'caution, as there are no checks for '
                                 'circularity. ')
        parser.add_argument('--allow-subrepositories', '-a',
                            dest='allow_subrepositories',
                            action='store_true', default=False,
                            help='When looking for repositories to add, '
                                 'keep searching within folders of existing '
                                 'repositories. ')

        parser.add_argument('path', nargs='?', default=None,
                            help='Rebuild and clean up the configuration '
                                 'file, removing empty groups. ')

        return parser.parse_args(args)

    def __call__(self):

        # if no paths are given, use the current path
        if not self.args.rebuild and self.args.path is None:
            self.args.path = os.getcwd()

        # clear the existing list if asked
        if self.args.clear:
            self.file.lines = []

        if self.args.path is not None:
            # find repositories in the given path add them
            for desc in finder.Finder.find_recursive(
                    self.args.path,
                    allow_links=self.args.follow_symlinks,
                    continue_in_repository=self.args.allow_subrepositories,
                    callback=lambda s: self.line.write(
                        format.Format.short_path(s, self.line.width))
            ):
                if not self.args.simulate:
                    self.line.linebreak()

                # print if we found a new repository
                if not self.file.contains(desc):
                    self.line.write(desc.path)
                    self.line.linebreak()
                    self.line.write("    {}".format(desc.source))
                    self.line.linebreak()

                self.file.insert_repo_or_get(desc)

        # if the rebuild flag is set, rebuild all the repos
        if self.args.rebuild:
            self.file.rebuild()

        if self.args.simulate:
            for line in self.file.lines:
                print(line.write())
        else:
            self.file.write()
