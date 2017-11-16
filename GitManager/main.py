#!/usr/bin/env python3

import argparse

from GitManager.utils import format
from GitManager.config import file
from GitManager.commands import status, lister, fetch, setup, pull, state, \
    push, reconfigure, gc, clone


def main(args):
    """ The main entry point for git-manager"""

    try:
        real_main(args)
    except BrokenPipeError:
        return 2
    except KeyboardInterrupt:
        print("\n{}".format(
            format.Format.red("Received KeyboardInterrupt")
        ))
        return 2
    except Exception as e:
        print("\n{}".format(
            format.Format.red("Unknown error: {}".format(e))
        ))
        return 3


def real_main(args):
    """ Main entry point for the program -- may throw errors"""

    ACTIONS = ['help', 'setup', 'clone', 'fetch', 'pull', 'push', 'gc', 'ls',
               'status', 'state', 'reconfigure']

    # Create an argument parser
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("action", nargs='?',
                        help="Action to perform. One of '{}'. ".format(
                            "', '".join(ACTIONS)))

    args, command_args = parser.parse_known_args()

    # Find the configuration file
    cfg_file = file.File.find()

    # Check that we have a configuration file.
    if cfg_file is None:
        print(format.Format.red("Missing configuration file. "))
        return 1

    # read the list of repositories
    config = file.File(cfg_file)
    try:
        config.read()
    except:
        print(format.Format.red("Unable to read configuration file. "))
        return 1

    line = format.TerminalLine()
    repos = list(config.repositories)

    if args.action == 'help' or args.action is None:
        parser.print_help()

    elif args.action == 'setup':
        setup.Setup(line, repos, *command_args)()
    elif args.action == 'clone':
        clone.Clone(line, config, *command_args)()

    elif args.action == 'fetch':
        fetch.Fetch(line, repos, *command_args)()
    elif args.action == 'pull':
        pull.Pull(line, repos, *command_args)()

    elif args.action == 'push':
        push.Push(line, repos, *command_args)()

    elif args.action == 'gc':
        gc.GC(line, repos, *command_args)()

    elif args.action == 'ls':
        lister.LsLocal(line, repos, *command_args)()
    elif args.action == 'status':
        status.Status(line, repos, *command_args)()
    elif args.action == 'state':
        state.State(line, repos, *command_args)()

    elif args.action == 'reconfigure':
        import sys
        line = format.TerminalLine(fd=sys.stderr)
        reconfigure.Reconfigure(line, config, *command_args)()

    else:
        print('Unknown command %r' % (args.action,))
        return 1

    return 0


__all__ = ["main"]
