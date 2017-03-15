from git import *
import os
import os.path as osp

curDir = os.getcwd()

def UpdateRepo(repoURL):
	# confirm or add .git to repo url
	if '.git' in repoURL:
		repoName = repoURL[repoURL.rfind("/") + 1 : -4]
	else:
		repoName = repoURL[repoURL.rfind("/") + 1 :]
		repoURL = repoURL + ".git"

	repoDir = osp.join(curDir, repoName)

	if(osp.exists(repoDir)):
		PullRepo(repoURL, repoName)
	else:
		CloneRepo(repoURL, repoName)
	

def CloneRepo(repoURL, repoName):
	repo = Repo.clone_from(repoURL, repoName, branch='master')


def PullRepo(repoURL, repoName):
	repo = Repo(osp.join(curDir, repoName))
	repo.remotes.origin.pull()


if __name__ == '__main__':
	repoURL = 'https://github.com/kanghuawu/my-test-repo.git'
	UpdateRepo(repoURL)

