import git
import os

currentDir = os.getcwd()

if(os.path.exists(currentDir + '/local_destination')):
	print "exist"

repo = git.Repo.clone_from(
  'https://github.com/sithu/assignment1-config-example',
  'local_destination',
  branch='master', depth=1,
  env={'GIT_SSL_NO_VERIFY': '1'},
)
