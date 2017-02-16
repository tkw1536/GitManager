#!/usr/bin/env python3

from GitManager.utils import format
from GitManager.config import file
from GitManager.commands import status, lister, fetch, setup, pull


#
# MAIN ENTRY POINT
#


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

    # Warn if we do not have anything to do
    if len(args) <= 1:
        print(
            format.Format.red("Too few arguments. Usage: %s"
                              "setup|fetch|pull|ls|status"
                              % (args[0])))
        return 1

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
    repos = list(config.descriptions)

    if args[1] == 'setup':
        setup.Setup(line, repos)()

    elif args[1] == 'fetch':
        fetch.Fetch(line, repos)()
    elif args[1] == 'pull':
        pull.Pull(line, repos)()

    elif args[1] == 'ls':
        lister.LsLocal(line, repos)()
    elif args[1] == 'status':
        status.Status(line, repos)()
    else:
        print('Unknown command %r' % (args[1],))
        return 1

    return 0


__all__ = ["main"]
