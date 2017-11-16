import typing

from . import description, implementation
import os.path


class Finder(object):
    """ Class that helps finding existing repositories """

    @staticmethod
    def find_recursive(path: str,
                       allow_links: bool=False,
                       continue_in_repository: bool=False,
                       callback:
                           typing.Callable[[str], None]=lambda s: None) \
            -> typing.Generator[description.RepositoryDescription, None, None]:
        """ Finds all repositories within a specific path
        :param path: Paths of repository to find
        :param allow_links: If True, continue searching in repositories even if
        they are symlinked. Use with caution, as this might cause the
        routine to run into a infinite loop
        :param continue_in_repository: If True, instead of stopping the
        recursing inside a repository, continue searching for sub-repositories
        :param callback: Optional callback to call when scanning a given
        directory.

        """

        # notify the caller that we are scanning path
        callback(path)

        # boolean indicating if we are inside a repository
        is_in_repo = False

        # if we do not allow links, stop when we have a link
        if not allow_links and os.path.islink(path):
            return

        # return the repository if available
        try:
            yield Finder.get_from_path(path)
            is_in_repo = True
        except ValueError:
            pass

        # if we got a repository, no need to continue iterating
        if is_in_repo and not continue_in_repository:
            return

        # iterate over all sub-items
        for name in os.listdir(path):

            # if we have a sub-directory
            dpath = os.path.join(path, name)
            if os.path.isdir(dpath):

                # iterate over the return items
                for desc in Finder.find_recursive(
                        dpath,
                        allow_links=allow_links,
                        continue_in_repository=continue_in_repository,
                        callback=callback):
                    yield desc

    @staticmethod
    def get_from_path(path: str) -> description.RepositoryDescription:
        """ Gets a single repository given a path if it exists
        :param path: Path to find repository at
        """

        # take the local repository
        local = implementation.LocalRepository(path)

        # if it doesn't exist, break
        if not local.exists():
            raise ValueError("No repository available in {}".format(path))

        # find the remote url -- try origin first
        try:
            remote_url = local.get_remote_url('origin')
        except ValueError:
            remotes = local.remotes
            if len(remotes) == 0:
                raise ValueError('No remotes available')

            # otherwise take the first remote
            remote_url = local.get_remote_url(remotes[0])

        # now we can be sure, the remote exists
        # so we can return the description
        return description.RepositoryDescription(remote_url, path)
