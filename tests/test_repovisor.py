import unittest
import os
from shutil import rmtree
from tempfile import mkstemp, mkdtemp
from repovisor import repovisor as rv
from git import Repo


def mktmp_git_dir():
    gitdir = mkdtemp()
    repo = Repo.init(gitdir)
    testfile, fpath = mkstemp(dir=gitdir, text=True)
    os.write(testfile, b'Test')
    os.close(testfile)
    repo.index.add([fpath])
    repo.index.commit("initial commit")
    return gitdir, repo, fpath


def rm_temp_gitdir(folder, repo, *files):
    rmtree(folder)
    del repo
    del folder
    for f in files:
        del f


class RepovisorTestCases(unittest.TestCase):
    def setUp(self):
        self.gitdir, self.repo, self.trackedfile = mktmp_git_dir()

    def tearDown(self):
        rm_temp_gitdir(self.gitdir, self.repo, self.trackedfile)

    def test_reposearch(self):
        repos = list(rv.reposearch(self.gitdir))
        self.assertEqual(self.gitdir, repos[0]['folder'])
        self.assertEqual(self.repo, repos[0]['pntr'])
        self.assertEqual('git', repos[0]['vcs'])

    def test_reposearch_empty(self):
        tmpdir = mkdtemp()
        repos = list(rv.reposearch(tmpdir))
        self.assertFalse(repos)
        rmtree(tmpdir)
