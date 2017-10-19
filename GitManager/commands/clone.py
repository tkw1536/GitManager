from GitManager.utils import format
from GitManager.config import file
from GitManager.repo import implementation, description
import os
import argparse


class Clone(object):
    """ A command to clone and optionally save a repository """

    def __init__(self, line: format.TerminalLine, config: file.File,
                 *commandargs):
        self.config = config
        self.line = line

        parser = argparse.ArgumentParser('Clones a repository as '
                                         'configured in the config '
                                         'file. ')
        parser.add_argument('--save', action='store_true', default=False)
        parser.add_argument('url', help='URL to clone')
        parser.add_argument('arguments', nargs=argparse.REMAINDER,
                            help='Extra arguments to pass to git clone '
                                 'command. ')
        self.args = parser.parse_args(commandargs)

    def url_to_description(self, url: str) \
            -> description.RepositoryDescription:
        """ Turns a URL into a repository description """

        remote = implementation.RemoteRepository(url)
        local = implementation.LocalRepository(
            os.path.join(self.config.root, *remote.components()))

        return description.RepositoryDescription(remote.url, local.path)

    def __call__(self):
        # get the path to clone into
        desc = self.url_to_description(self.args.url)

        if desc.local.exists():
            self.line.write('Repository already exists, nothing to clone. ')
            return

        # if requested, save it
        if self.args.save:
            self.config.insert_repo_or_get(desc)
            self.config.write()

        desc.remote.clone(desc.local, *self.args.arguments)
