#!/usr/bin/env python3

from GitManager.format import Format
from GitManager.vcs import Git
from GitManager.config import Config

import os
import os.path
import sys

#
# Abstractions
#


def do_clone(repos):
    """ Runs the clone command over all repositories. """

    for (source, cwd, name) in repos:
        folder = Git.tuple_to_path(source, cwd, name)
        if Git.exist_local(folder):
            print('%s %s == %s' % (Format.red('clone'), source, folder))
        else:
            print('git %s %s -> %s' % (Format.green('clone'), source, folder))
            Git.clone(source, folder)


def do_pull(repos):
    """ Runs the pull command over all repositories. """

    for (source, cwd, name) in repos:
        folder = Git.tuple_to_path(source, cwd, name)
        if not Git.exist_local(folder):
            print('%s %s -> %s' % (Format.red('pull'), source, folder))
        else:
            print(Format.green(folder))
            Git.pull(folder)


def do_push(repos):
    """ runs the push commmand over all repositories. """

    for (source, cwd, name) in repos:
        folder = Git.tuple_to_path(source, cwd, name)
        if not Git.exist_local(folder):
            print(Format.red(folder))
        else:
            print(Format.green(folder))
            Git.push(folder)


def do_ls(repos):
    for (source, cwd, name) in repos:
        folder = Git.tuple_to_path(source, cwd, name)
        if Git.exist_local(folder):
            print(Format.green(folder))
        else:
            print(Format.red(folder))

#
# MAIN ENTRY POINT
#


def main(args):
    """ The main entry point for git-manager"""

    # Warn if we do not have anything to do
    if len(args) <= 1:
        print(Format.red("Too few arguments. Usage: %s clone|pull|push|ls"
                         % (args[0])))
        sys.exit(1)

    # Which file to use
    # TODO: Check other locations.
    cfg_file = os.path.expanduser('~/.gitmanager')

    # read the list of repositories
    # TODO: Have a human readable error when failing.
    with open(cfg_file, 'r') as f:
        repos = Config.parse_lines(f.readlines())

    # Print some general info
    print(Format.cyan('%s: %d repos' % (cfg_file, len(repos))))

    if args[1] == 'clone':
        do_clone(repos)
    elif args[1] == 'pull':
        do_pull(repos)
    elif args[1] == 'push':
        do_push(repos)
    elif args[1] == 'ls':
        do_ls(repos)
    else:
        print('Unknown command %r' % (args[1], ))
        sys.exit(1)

__all__ = ["main"]

