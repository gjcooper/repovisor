from repovisor import repovisor as rv
import click


@click.group()
@click.version_option()
def main():
    pass


@main.command(name='search')
@click.argument('folders', nargs=-1, type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option('--brief', '-b', is_flag=True, help='Use the short form of reporting status')
def __search_action(folders, brief):
    '''search through a set of folders and print status for them'''
    for repo in rv.reposearch(*folders):
        rv.print_repo(repo, brief=brief)
