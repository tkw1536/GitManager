#!/usr/bin/env python3

from GitManager.format import Format, TerminalLine
from GitManager.vcs import Git
from GitManager.config import Config

import os
import os.path

#
# Abstractions
#

def prepare_terminal_line(repos):
    """ Makes a format string for a given set of repositories. """

    # Create a new terminal line for output
    t = TerminalLine()

    # Prepare format strings for each repository
    repo_count = str(len(repos))
    repo_fmt_str = "[%%0%sd/%s] %%s" % (len(repo_count), repo_count)
    l_fmt_str = 2 * len(repo_count) * 2 + 4

    return (t, repo_fmt_str, l_fmt_str, repo_count)


def do_clone(repos):
    """ Runs the clone command over all repositories. """

    (t, repo_fmt_str, l_fmt_str, repo_count) = prepare_terminal_line(repos)

    for (i, (source, cwd, name)) in enumerate(repos):

        folder = Git.tuple_to_path(source, cwd, name)
        human = Format.path(folder, t.width - l_fmt_str)

        if Git.exist_local(folder):
            t.write(repo_fmt_str % (i, Format.cyan(human)))
        else:
            t.write((repo_fmt_str % (i, Format.green(human))))
            t.append('\n')

            Git.clone(source, cwd, folder)

    # And write a new line
    t.write('Finished processing %s repositories. \n' % repo_count)


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
        return 1

    # Find the configuration file
    cfg_file = Config.find_config_file()

    # Check that we have a configuration file.
    if cfg_file is None:
        print(Format.red("Missing configuration file. "))
        return 1

    # Which file to use
    # TODO: Check other locations.
    cfg_file = os.path.expanduser('~/.gitmanager')

    # read the list of repositories
    # TODO: Have a human readable error when failing.
    with open(cfg_file, 'r') as f:
        repos = Config.parse_lines(f.readlines())

    # Print some general info
    # print(Format.cyan('%s: %d repos' % (cfg_file, len(repos))))

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
        return 1

    return 0

__all__ = ["main"]

