from .repostate import GitRepoState
from git.exc import InvalidGitRepositoryError, GitCommandError
from pathlib import Path
import os
import click


def pathlen(path):
    """Return folder level of the path string"""
    return len(Path(path).parts)


def reposearch(*folders, prune=False, level=0):
    for folder in folders:
        for dir, subdirs, files in os.walk(folder):
            try:
                yield (pathlen(dir) - pathlen(folder)), GitRepoState(dir)
                if prune:
                    subdirs[:] = []
                else:
                    subdirs[:] = [s for s in subdirs if s != '.git']
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


def branch_uptodate(branch, true_on_missing_origin=True):
    """Return True is branch is up to date with origin, otherwise False,
    also returns True if no remote defined"""
    if branch['upstream']:
        if branch['ahead'] or branch['behind']:
            return False
        return True
    if true_on_missing_origin:
        return True
    return False
    
def long_state_representation(repo):
    """Print the state for a repository"""
    loc = 'Location: ' + repo.path
    state = repo.state
    mod = 'Modified: {}'.format(click.style('Yes', fg='red') if state['dirty'] else click.style('No', fg='green'))
    untracked = 'Untracked: {}'.format(click.style(str(state['untracked']), fg='yellow'))
    refs = 'Branches: \n'
    refs += '\n'.join([branch_representation(b) for b in state['refcheck']])
    return '\n'.join([loc, mod, untracked, refs])


def repo_view(repo, brief=False):
    """Print all repo current state to terminal"""
    surrounds = '-' * 40 + '\n{}\n' + '-' * 40
    try:
        view = short_state_representation(repo) if brief else surrounds.format(long_state_representation(repo))
    except GitCommandError as gce:
        if 'must be run in a work tree' in gce.stderr:
            if brief:
                loc = repo.path
                msg = click.style('Bare repo', fg='yellow')
                view = ' '.join([loc, msg])
            else:
                loc = 'Location: ' + repo.path
                msg = click.style('Repository is bare and does not have state to track', fg='yellow')
                view = surrounds.format('\n'.join([loc, msg]))
    return view
