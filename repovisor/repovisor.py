from .repostate import GitRepoState
from git.exc import InvalidGitRepositoryError
from colorama import Fore, Style, init
import os

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


def branch_representation(branch):
    refview = '  Name: {:10.10} Upstream: '.format(branch['name'])
    if branch['upstream']:
        refview += '{!s:17.17} Status: {!s}'.format(branch['upstream'],
                                                    ahead_behind(branch))
    else:
        refview += Fore.YELLOW + 'None' + Style.RESET_ALL
    return refview


def state_representation(repo):
    """Print the state for a repository"""
    loc = 'Location: ' + repo.path
    state = repo.state
    mod = 'Modified: '
    if state['dirty']:
        mod += Fore.RED + 'Yes' + Style.RESET_ALL
    else:
        mod += Fore.GREEN + 'No' + Style.RESET_ALL
    untracked = 'Untracked: ' + Fore.YELLOW
    untracked += str(state['untracked']) + Style.RESET_ALL
    refs = 'Branches: \n'
    refs += '\n'.join([branch_representation(b) for b in state['refcheck']])
    return '\n'.join([loc, mod, untracked, refs])


def print_all(*repos):
    """Print all repo current state to terminal"""
    for repo in repos:
        print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
        print(state_representation(repo))
        print('________________________________________')
