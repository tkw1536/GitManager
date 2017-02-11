import re
import os.path


class Config(object):
    """ Methods for parsing and reading configuration file. """

    def __init__(self):
        """ Prevents creation of Config(). """

        raise TypeError("Config() can not be instantiated")

    @staticmethod
    def find_config_file():
        """Finds the location of the Configuration File.

        :rtype: str
        """

        # 1. Check $GIT_MANAGER_CONFIG if set
        if "GIT_MANAGER_CONFIG" in os.environ:
            git_manager_config = os.environ["GIT_MANAGER_CONFIG"]

            if os.path.isfile(git_manager_config):
                return git_manager_config

        # 2. ~/.config/.gitmanager/config (or $XDG_CONFIG_HOME/.gitmanager/config if set)
        if "XDG_CONFIG_HOME" in os.environ:
            xdg_config_home = os.environ["XDG_CONFIG_HOME"]
        else:
            xdg_config_home = os.path.join(os.path.expanduser("~"), ".config")

        xdg_config_path = os.path.join(xdg_config_home, ".gitmanager",
                                       "config")
        if os.path.isfile(xdg_config_path):
            return xdg_config_path

        # 3. ~/.gitmanager
        fallback_path = os.path.join(os.path.expanduser("~"), ".gitmanager")
        if os.path.isfile(fallback_path):
            return fallback_path

        # No configuration file found -- raise an error
        return None

    @staticmethod
    def parse_lines(lines):
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
                previous_item = REPO_STACK[new_order - 1]

                # find out the new items
                new_sub_dir = os.path.join(previous_item[0], sub_dir)
                new_clone_uri = previous_item[1].replace('%s', clone_uri)

                # Expand it into the new one
                REPO_STACK[new_order:] = [(new_sub_dir, new_clone_uri)]

                continue

            m_repo = DIRECTIVE_REPO.match(l)
            if m_repo:
                repo_group = REPO_STACK[-1]

                # Extract the source URI of the previous item
                source_uri = repo_group[1].replace('%s', m_repo.group(1))

                # And the path to clone to
                folder = m_repo.group(3) or None
                path = os.path.expanduser(os.path.join(repo_group[0], folder)) \
                    if folder is not None else None

                # Find the current working directory
                cwd = repo_group[0]

                # And append the repo
                REPO_LIST.append((source_uri, cwd, path))

                continue

            raise Exception('Unable to parse line. ')

        return REPO_LIST


__all__ = ["Config"]
