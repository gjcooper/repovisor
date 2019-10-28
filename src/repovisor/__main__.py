from repovisor import repovisor as rv
import click


@click.group()
@click.version_option()
def main():
    pass


@main.command(name='search')
@click.argument('folders', nargs=-1, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option('--brief', '-b', is_flag=True, help='Use the short form of reporting status')
@click.option('--prune', '-p', is_flag=True, help='Prune directories as soon as we reach a repository')
@click.option('--tree', '-t', is_flag=True, help='Show repositories in a tree structure, only used if brief is also selected')
@click.option('--hide', is_flag=True, help='Hide repositories that are clean')
@click.option('--remote', is_flag=True, help='Warn if repo has no remote')
def __search_action(folders, brief, prune, tree, hide, remote):
    '''search through a set of folders and print status for them'''
    for repo_level, repo in rv.reposearch(*folders, prune=prune, level=0):
        view = rv.repo_view(repo, brief=brief)
        if tree and brief:
            view = '-'*repo_level + view
        if hide and not repo.bare:
            if not repo.state['dirty']:
                if not repo.state['untracked']:
                    if all(rv.branch_uptodate(b, true_on_missing_origin=not remote) for b in repo.state['refcheck']):
                        continue
        print(view)
