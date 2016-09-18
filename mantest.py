from repovisor import repovisor
repos = list(repovisor.reposearch('.'))
repovisor.addHandlers()
repovisor.repocheck(*repos)
print(repos)
repovisor.print_state(*repos)
