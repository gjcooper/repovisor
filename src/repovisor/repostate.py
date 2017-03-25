from git import Repo
from git.exc import InvalidGitRepositoryError
from colorama import Fore, Style, init
import os
import warnings

init()

class GitRepoState(Repo):
    """An object that represents the state of a repository"""
    def __init__(self, directory, **kwargs):
        self.path = os.path.abspath(directory)
        super().__init__(self.path, **kwargs)

    def check_upstream(self, ref):
        """replicate my for-each-ref pattern"""
        upstream = ref.tracking_branch()
        if not upstream:
            return dict(name=ref.name, upstream=None)
        ahead = sum(1 for c in
                    self.iter_commits(rev=upstream.name + '..' + ref.name))
        behind = sum(1 for c in
                     self.iter_commits(rev=ref.name + '..' + upstream.name))
        return dict(name=ref.name, upstream=upstream, ahead=ahead,
                    behind=behind)

    def _checkall_upstreams(self):
        """Check a git repo state and report it"""
        return [self.check_upstream(ref) for ref in self.heads]

    @property
    def state(self):
        """Return the current state for this repository"""
        return {
            'dirty': self.is_dirty(),
            'untracked': self.untracked_files,
            'refcheck': self._checkall_upstreams()
            }
        
