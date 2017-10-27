from .repostate import GitRepoState
from git.exc import InvalidGitRepositoryError
import os
from colorama import Fore, Style
import click


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


def branch_representation(branch, brief=False):
    if brief:
        refview = branch['name'] + ' '
    else:
        refview = '  Name: {:10.10} Upstream: '.format(branch['name'])
    if branch['upstream']:
        if brief:
            refview += '[{}]'.format(ahead_behind(branch))
        else:
            refview += '{!s:17.17} Status: {!s}'.format(branch['upstream'],
                                                        ahead_behind(branch))
    else:
        refview += Fore.YELLOW + 'None' + Style.RESET_ALL
    return refview


def short_state_representation(repo):
    """Print the state for a repository"""
    loc = repo.path
    state = repo.state
    mod = ''
    if state['dirty']:
        mod += Fore.RED + 'Modified' + Style.RESET_ALL
    else:
        mod += Fore.GREEN + 'Clean' + Style.RESET_ALL
    untracked = 'Untracked: ' + Fore.YELLOW
    if len(state['untracked']) > 3:
        untracked += '[ {}, {}, {}, ... ]'.format(*state['untracked'][:3]) + Style.RESET_ALL
    else:
        untracked += str(state['untracked']) + Style.RESET_ALL
    refs = 'Branches: '
    refs += ' '.join([branch_representation(b, brief=True) for b in state['refcheck']])
    return ' '.join([loc, mod, untracked, refs])


def long_state_representation(repo):
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


def print_repo(repo, brief=False):
    """Print all repo current state to terminal"""
    if brief:
        print(short_state_representation(repo))
        return
    print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    print(long_state_representation(repo))
    print('________________________________________')
