from git import Repo
from git.exc import InvalidGitRepositoryError
import os

def reposearch(*folders):
    for folder in folders:
        for dir, subdirs, files in os.walk(folder):
            try:
                yield dict(vcs='git', pntr=Repo(dir), folder=dir)
                subdirs[:] = []
                continue
            except InvalidGitRepositoryError:
                pass

