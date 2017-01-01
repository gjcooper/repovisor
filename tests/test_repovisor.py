import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory
from repovisor import repovisor as rv
from colorama import Fore, Style, init
from repovisor.repostate import GitRepoState
from git.exc import InvalidGitRepositoryError

init()


def mktmp_git_dir():
    gitdir = TemporaryDirectory()
    repo = GitRepoState.init(gitdir.name)
    initfile = NamedTemporaryFile(dir=gitdir.name, delete=False)
    initfile.write(b'Test')
    initfile.close()
    repo.index.add([initfile.name])
    repo.index.commit('initial commit')
    return gitdir, repo, initfile


def mkbare_git_dir():
    gitdir = TemporaryDirectory()
    repo = GitRepoState.init(gitdir.name, bare=True)
    return gitdir, repo


class RepovisorTestCases(unittest.TestCase):
    def setUp(self):
        self.gitdir, self.repo, self.trackedfile = mktmp_git_dir()
        self.baredir, self.bare = mkbare_git_dir()

    def tearDown(self):
        pass

    def test_reposearch(self):
        repos = list(rv.reposearch(self.gitdir.name))
        self.assertEqual(self.gitdir.name, repos[0].working_dir)
        self.assertEqual(self.repo, repos[0])

    def test_reposearch_empty(self):
        tmpdir = TemporaryDirectory()
        repos = list(rv.reposearch(tmpdir.name))
        self.assertFalse(repos)

    def test_repoinit(self):
        # Test that an unknown vcs raises a warning
        td = TemporaryDirectory()
        with self.assertRaises(InvalidGitRepositoryError):
            GitRepoState(td.name)

    def test_branch_representation_no_upstream(self):
        noup_view = '  Name: {:10.10} Upstream: '.format('master')
        noup_view += Fore.YELLOW + 'None' + Style.RESET_ALL
        masterref = self.repo.heads.master
        noup_git = rv.branch_representation(self.repo.check_upstream(masterref))
        self.assertEqual(noup_git, noup_view)

    def test_branch_representation_with_upstream(self):
        up_view = '  Name: {:10.10} Upstream: {!s:17.17} Status: {!s}'
        up_filler = ['master', 'origin/master', '-/-']
        ahead = Fore.RED + '+1' + Style.RESET_ALL + '/-'
        behind = '-/' + Fore.RED + '-1' + Style.RESET_ALL
        masterref = self.repo.heads.master
        # Add tracking branch and remote
        origin = self.repo.create_remote('origin', self.baredir.name)
        origin.push(refspec='master')
        self.repo.refs.master.set_tracking_branch(origin.refs.master)
        # Grab for_each_ref on base versions
        up_git = rv.branch_representation(self.repo.check_upstream(masterref))
        self.assertEqual(up_git, up_view.format(*up_filler))
        # Add new temp file to local repo
        tempfile = NamedTemporaryFile(dir=self.gitdir.name, delete=False)
        self.repo.index.add([tempfile.name])
        self.repo.index.commit('Commit2')
        # Check we are now ahead by one commit
        up_git = rv.branch_representation(self.repo.check_upstream(masterref))
        up_filler[2] = ahead
        self.assertEqual(up_git, up_view.format(*up_filler))
        # Push the new file then revert the local repo
        origin.push()
        self.repo.refs.master.set_commit('HEAD~1')
        # Now check it is behind
        up_git = rv.branch_representation(self.repo.check_upstream(masterref))
        up_filler[2] = behind
        self.assertEqual(up_git, up_view.format(*up_filler))

    def test_print_state(self):
        pass
