from git import *
import os
import os.path as osp

curDir = os.getcwd()
repoName = ""
repDir = ""
repoURL = ""

def UpdateRepo(repoURL):
	# confirm or add .git to repo url
	# if ".git" in repoURL:
	# 	repoName = repoURL[repoURL.rfind("/") + 1 : -4]
	# else:
	# 	repoName = repoURL[repoURL.rfind("/") + 1 :]
	# 	repoURL = osp.join(curDir, ".git")

	repDir = osp.join(curDir, 'my-test-repo')
	repo = Repo(repoURL)

	repoDir = osp.join(curDir, repoName)
	if(osp.exists(repoDir)):
		PullRepo(repo)
	else:
		CloneRepo(repo)
	
def CloneRepo(repo):
	cloned_repo = Repo.clone(osp.join(curDir, 'my-test-repo'), "v1")
	# repo = Repo.clone_from(
	# repoURL,
	# repoName,
	# branch='master', depth=1,
	# env={'GIT_SSL_NO_VERIFY': '1'},
	# )

def PullRepo(repo):
	repo.remotes.origin.pull()

repoURL = "https://github.com/kanghuawu/my-test-repo"
UpdateRepo(repoURL)
# assert not repo.bare

# cloned_repo = repo.clone(osp.join(curDir, 'my-test-repo'))
# assert cloned_repo.__class__ is Repo


