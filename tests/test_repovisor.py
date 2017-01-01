import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory
from repovisor import repovisor as rv
from git import Repo


def mktmp_git_dir():
    gitdir = TemporaryDirectory()
    repo = Repo.init(gitdir.name)
    initfile = NamedTemporaryFile(dir=gitdir.name, delete=False)
    initfile.write(b'Test')
    initfile.close()
    repo.index.add([initfile.name])
    repo.index.commit('initial commit')
    return gitdir, repo, initfile


def mkbare_git_dir():
    gitdir = TemporaryDirectory()
    repo = Repo.init(gitdir.name, bare=True)
    return gitdir, repo


class RepovisorTestCases(unittest.TestCase):
    def setUp(self):
        self.gitdir, self.repo, self.trackedfile = mktmp_git_dir()
        self.repodict = dict(folder=self.gitdir.name,
                             vcs='git',
                             pntr=self.repo)
        self.baredir, self.bare = mkbare_git_dir()

    def tearDown(self):
        pass

    def test_reposearch(self):
        repos = list(rv.reposearch(self.gitdir.name))
        self.assertEqual(self.gitdir.name, repos[0]['folder'])
        self.assertEqual(self.repo, repos[0]['pntr'])
        self.assertEqual('git', repos[0]['vcs'])

    def test_reposearch_empty(self):
        tmpdir = TemporaryDirectory()
        repos = list(rv.reposearch(tmpdir.name))
        self.assertFalse(repos)

    def test_repocheck(self):
        # Test that an unknown vcs raises a warning
        unknowndict = {'vcs': 'navcs', 'pntr': None, 'folder': 'Fake'}
        with self.assertWarnsRegex(UserWarning, 'Unknown vcs type'):
            rv.repocheck(unknowndict)
        # Test that repo state is passed back
        rv.repocheck(self.repodict)
        rv.repocheck(self.repodict)
        self.assertEqual(self.repodict['state'], self.repodict['laststate'])

    def test_git_for_each_ref_no_upstream(self):
        noup_git = rv.git_for_each_ref(self.repo, self.repo.heads.master)
        self.assertEqual(noup_git, {'name': 'master', 'upstream': None})

    def test_git_for_each_ref_with_upstream(self):
        # Add tracking branch and remote
        origin = self.repo.create_remote('origin', self.baredir.name)
        origin.push(refspec='master')
        self.repo.refs.master.set_tracking_branch(origin.refs.master)
        # Grab for_each_ref on base versions
        up_git = rv.git_for_each_ref(self.repo, self.repo.heads.master)
        self.assertEqual(up_git['ahead'], 0)
        self.assertEqual(up_git['behind'], 0)
        # Add new temp file to local repo
        tempfile = NamedTemporaryFile(dir=self.gitdir.name, delete=False)
        self.repo.index.add([tempfile.name])
        self.repo.index.commit('Commit2')
        # Check we are now ahead by one commit
        up_git = rv.git_for_each_ref(self.repo, self.repo.heads.master)
        self.assertEqual(up_git['ahead'], 1)
        # Push the new file then revert the local repo
        origin.push()
        self.repo.refs.master.set_commit('HEAD~1')
        # Now check it is behind
        up_git = rv.git_for_each_ref(self.repo, self.repo.heads.master)
        self.assertEqual(up_git['behind'], 1)

    def test_print_state(self):
        pass
