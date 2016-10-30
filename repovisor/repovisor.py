from .repostate import GitRepoState
from git import Repo
from git.exc import InvalidGitRepositoryError
from colorama import Fore, Style, init
import os
import warnings

init()


def reposearch(*folders):
    for folder in folders:
        for dir, subdirs, files in os.walk(folder):
            try:
                yield GitRepoState(dir)
                subdirs[:] = []
                continue
            except InvalidGitRepositoryError:
                pass


def repocheck(*repos):
    for repo in repos:
        if 'state' in repo:
            repo['laststate'] = repo['state']
        try:
            repo['state'] = vcs_statechecker(repo['vcs'])(repo['pntr'])
        except KeyError:
            warnings.warn(
                'Unknown vcs type: {} not checked'.format(repo['folder']))


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
        print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
        print('Location: ', repo['folder'])
        state = repo['state']
        print('Modified: ', Fore.RED, state['dirty'], Style.RESET_ALL)
        print('Untracked: \n', Fore.YELLOW, '\n'.join(state['untracked']),
              Style.RESET_ALL)
        print('Refs:')
        for ref in state['refcheck']:
            ab_notifier = ''
            if ref['upstream']:
                ab_notifier = ahead_behind(ref)
            print('\tName: ', ref['name'], ' Upstream: ', ref['upstream'],
                  'Status: ', ab_notifier)
        print('________________________________________')
