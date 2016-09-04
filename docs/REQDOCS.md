Format
======

Git Repo found (dir)
Remotes:
	_____	(fetch)
	_____	(push)

---

Status
	On branch <--->
	Your branch is up to date OR
	Changes not staged to commit OR
	Your branch is ahead/behind(?) OR
	Changes to be committed

---

BRANCHES:
	(local)	UPSTREAM <upstream>	STATUS	<status>


---

Working Ideas
=============

Initial project and working set of code can be found in this [gist](https://gist.github.com/gjcooper/479ddeb59558120c34adf5deb90dd58)

Basic premise of this rough script is to walk a directory tree and determine git repositories (.git) in subdirectories <sup>[1](#fn_gitdetect)</sup>. Once there it runs some git commands using subprocess library. In particular the git remote, git status and git for-each-ref commands<sup>[2](#fn_gitcmd)</sup>. The output is formatted with ANSI colour codes to slightly prettify it.



<a name="fn_gitdetect">1</a>: Find out how to accurately detect that a dir is a git repo
<a name="fn_gitcmd">2</a>: Pretty sure for-each-ref is the only command I'll need. Need to check mater/laptop machine for all available commands.

