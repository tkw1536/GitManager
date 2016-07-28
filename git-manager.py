#!/usr/bin/env python3

import re
import subprocess
import os
import sys
import os.path

from typing import List, Tuple

#
# CONFIG FILE PARSER
#

def to_humanish_name(uri: str) -> str:
    """
    Turns a git URI into a 'humanish' URI.

    :param uri: URI to parse.
    """

    # Trim a trailing '.git'
    if uri.endswith('.git'):
        human = uri[:-4]
    else:
        human = uri

    # Trim trailing '/'s
    while human.endswith('/'):
        human = human[:-1]

    # And take the last part of the path.
    if '/' in human:
        human = human.split('/')[-1]

    # and return
    return human


def parse_config_lines(lines: List[str]) -> List[Tuple[str, str]]:
    """
    Parses a configuration file

    :param lines: Lines representing the configuration file.
    :return: a list of git repositories
    """

    # REGULAR EXPRESSIONS
    DIRECTIVE_NOP = re.compile(r'^((\s*)#(.*))|(\s*)$')
    DIRECTIVE_BASE = re.compile(r'\s*(>+)\s+([^\s]+)(\s+([^\s]+))?\s*$')
    DIRECTIVE_REPO = re.compile(r'^\s*([^>\s]+)(\s+([^\s]+))?\s*$')

    # A list of repos and origins
    REPO_LIST = []

    # A stack for repo folders
    REPO_STACK = [('~', '%s')]

    for l in lines:
        # Just a comment, do nothing.
        if DIRECTIVE_NOP.match(l):
            continue

        # Check if we have a base command.
        m_base = DIRECTIVE_BASE.match(l)
        if m_base:

            # Parse the orders
            current_order = len(REPO_STACK)
            new_order = len(m_base.group(1))

            # Check that we are not skipping a level
            if new_order > current_order:
                raise Exception(
                    'Unable to parse config file: Missing base sublevel. ')

            # Read the subdirectory and origin path
            sub_dir = m_base.group(2)
            clone_uri = m_base.group(4) or '%s'


            # Now take the previous item.
            previous_item = REPO_STACK[new_order-1]

            new_sub_dir = os.path.join(previous_item[0], sub_dir)
            new_clone_uri = previous_item[1].replace('%s', clone_uri)

            # Expand it into the new one
            REPO_STACK[new_order:] = [(new_sub_dir, new_clone_uri)]

            continue

        m_repo = DIRECTIVE_REPO.match(l)
        if m_repo:
            previous_item = REPO_STACK[-1]

            # Get the source URI of the repo
            source_uri = previous_item[1].replace('%s', m_repo.group(1))

            # And the folder to clone to
            folder = os.path.join(previous_item[0], m_repo.group(3) or to_humanish_name(source_uri))

            # And append the repo
            REPO_LIST.append((source_uri, os.path.expanduser(folder)))

            continue

        raise Exception('Unable to parse line. ')

    return REPO_LIST

#
# GIT INTERFACE
#


def has_git_at(folder: str) -> bool:
    """ Checks if there is a git repository in the given folder.

    :param folder: Folder to check for.
    """

    # Check if it is a folder.
    if not os.path.isdir(folder):
        return False

    # make two pipes to silence everything
    pipeA = open(os.devnull, 'wb')
    pipeB = open(os.devnull, 'wb')

    # and check if it exists there
    return subprocess.call(["git", "rev-parse"], stdout=pipeA, stderr=pipeB) == 0


def make_new_clone(folder: str, source: str) -> int:
    """
    Makes a new git clone at a given folder.

    :param folder:
    :param source:
    :return:
    """

    # ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # and make the clone.
    return subprocess.call(["git", "clone", source, folder])


def git_pull(folder: str) -> int:
    """ Runs git pull in a certain folder.

    :param folder:
    """

    return subprocess.call(["git", "pull"], cwd=folder)


def git_push(folder: str) -> int:
    """ Runs git push in a certain folder.

    :param folder:
    """

    return subprocess.call(["git", "push"], cwd=folder)

#
# Abstractions
#


def do_clone(repos: List[Tuple[str, str]]) -> None:
    """ Runs the clone command over all repositories. """

    for (source, folder) in repos:
        if has_git_at(folder):
            print('Skipping %s: Folder already has a git repository. ')
        else:
            print('clone %s @ %s' % (source, folder))
            make_new_clone(folder, source)


def do_pull(repos: List[Tuple[str, str]]) -> None:
    """ Runs the pull command over all repositories. """

    for (source, folder) in repos:
        if not has_git_at(folder):
            print('Skipping %s: No local clone to pull. ')
        else:
            print('pull %s @ %s' % (source, folder))
            git_pull(folder)

def do_push(repos):
    """ runs the push commmand over all repositories. """

    for (source, folder) in repos:
        if not has_git_at(folder):
            print('Skipping %s: No local clone to push. ')
        else:
            print('push %s @ %s' % (source, folder))
            git_push(folder)

def do_ls(repos):
    for (source, folder) in repos:
        if has_git_at(folder):
            print('%s @ %s' % (source, folder))

#
# MAIN ENTRY POINT
#


def main(args):

    # Warn if we do not have anything to do
    if len(args) <= 1:
        print("Too few arguments. Usage: %s clone|pull|push|ls" % (args[0]))
        sys.exit(1)

    # Which file to use
    cfg_file = os.path.expanduser('~/.gitrepos')

    # read the list of repositories
    with open(cfg_file, 'r') as f:
        repos = parse_config_lines(f.readlines())

    # Print some general info
    print('%s repositories loaded from %s' % (len(repos), cfg_file))

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

if __name__ == '__main__':
    main(sys.argv)