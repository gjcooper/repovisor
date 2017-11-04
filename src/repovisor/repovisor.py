from .repostate import GitRepoState
from git.exc import InvalidGitRepositoryError
import os
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
    return '{}/{}'.format(
        click.style('+' + str(ref['ahead']), fg='red') if ref['ahead'] else '-',
        click.style('-' + str(ref['behind']), fg='red') if ref['behind'] else '-')


def branch_representation(branch, brief=False):
    if branch['upstream']:
        if brief:
            refview = '{:.10} [{}]'.format(branch['name'], ahead_behind(branch))
        else:
            refview = '  Name: {:10.10} Upstream: {!s:17.17} Status: {!s}'.format(
                branch['name'], branch['upstream'], ahead_behind(branch))
    else:
        refview = '{:.10} {}' if brief else '  Name: {:10.10} Upstream: '
        refview = refview.format(branch['name'], click.style('None', fg='yellow'))
    return refview


def short_state_representation(repo):
    """Print the state for a repository"""
    loc = repo.path
    state = repo.state
    mod = click.style('Modified', fg='red') if state['dirty'] else click.style('Clean', fg='green')
    untracked = 'Untracked: '

    if len(state['untracked']) > 3:
        untracked += click.style('[ {}, {}, {}, ... ]'.format(*state['untracked'][:3]), fg='yellow')
    else:
        untracked += click.style(str(state['untracked']), fg='yellow')
    refs = 'Branches: '
    refs += ' '.join([branch_representation(b, brief=True) for b in state['refcheck']])
    return ' '.join([loc, mod, untracked, refs])


def long_state_representation(repo):
    """Print the state for a repository"""
    loc = 'Location: ' + repo.path
    state = repo.state
    mod = 'Modified: {}'.format(click.style('Yes', fg='red') if state['dirty'] else click.style('No', fg='green'))
    untracked = 'Untracked: {}'.format(click.style(str(state['untracked']), fg='yellow'))
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
