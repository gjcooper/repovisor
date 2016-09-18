from git import Repo
from git.exc import InvalidGitRepositoryError
from colorama import Fore, Style, init
import os
import warnings

vcs_statechecker = {'git': None}
init()


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


def ahead_behind(ref):
    if ref['ahead']:
        glyph = Fore.RED + '+' + str(ref['ahead']) + Style.RESET_ALL
    else:
        glyph = '-'
    glyph += '/'
    if ref['behind']:
        glyph += Fore.RED + '-' + str(ref['behind']) + Style.RESET_ALL
    else:
        glyph += '-'
    return glyph


def print_state(*repos):
    """Print all repo current state to terminal"""
    for repo in repos:
        print('Location: ', repo['folder'])
        state = repo['state']
        print('Modified: ', Fore.RED, state['dirty'], Style.RESET_ALL)
        print('Untracked: ', Fore.YELLOW, '\n'.join(state['untracked']),
              Style.RESET_ALL)
        print('Refs:')
        for ref in state['refcheck']:
            ab_notifier = ''
            if ref['upstream']:
                ab_notifier = ahead_behind(ref)
            print('\tName: ', ref['name'], ' Upstream: ', ref['upstream'],
                  'Status: ', ab_notifier)