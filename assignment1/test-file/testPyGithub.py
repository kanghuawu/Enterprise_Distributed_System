import github

git = github.PyGithub()
org = git.get_organization('OrgName')
repo = org.get_repo('repo-name')
pr = repo.get_pull(1)
print 'PR author: %s' % pr.user.login
comments = pr.get_issue_comments()
for comment in comments:
  print 'Comment: ', comment.created_at, comment.user.login, comment.body
pr.create_issue_comment('Comment from GITHUB_TOKEN user') # aka git.get_user()
