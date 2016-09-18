from git import Repo
from git.exc import InvalidGitRepositoryError
import os
import warnings

vcs_statechecker = {'git': None}


def reposearch(*folders):
    for folder in folders:
        for dir, subdirs, files in os.walk(folder):
            try:
                yield dict(vcs='git', pntr=Repo(dir), folder=dir)
                subdirs[:] = []
                continue
            except InvalidGitRepositoryError:
                pass


def repocheck(*repos):
    for repo in repos:
        if 'state' in repo:
            repo['laststate'] = repo['state']
        if repo['vcs'] not in vcs_statechecker:
            warnings.warn(
                'Unknown vcs type: {} not checked'.format(repo['folder']))
        repo['state'] = vcs_statechecker[repo['vcs']](repo['pntr'])


def git_for_each_ref(repo, ref):
    """replicate my for-each-ref pattern"""
    upstream = ref.tracking_branch()
    if not upstream:
        return dict(name=ref.name, upstream=None)
    ahead = sum(1 for c in
                repo.iter_commits(rev=upstream.name + '..' + ref.name))
    behind = sum(1 for c in
                 repo.iter_commits(rev=ref.name + '..' + upstream.name))
    return dict(name=ref.name, upstream=upstream, ahead=ahead, behind=behind)


def checkGit(repo):
    """Check a git repo state and report it"""
    dirty = repo.is_dirty()
    untracked = repo.untracked_files
    reflist = [git_for_each_ref(repo, ref) for ref in repo.heads]
    return dict(dirty=dirty, untracked=untracked, refcheck=reflist)


def addHandlers():
    """add statechker handlers to dict"""
    vcs_statechecker['git'] = checkGit
