from flask import Flask, jsonify, make_response
import sys
import yaml
import json
from git import *
import os
import os.path as osp

curDir = os.getcwd()

app = Flask(__name__)

@app.route("/v1/<file>")

def getConfigFile(file):

	repoURL = app.config.get('repoURL')
	print repoURL
	if(repoURL != None):
		repo = UpdateRepo(repoURL)
	else:
		return make_response('Need three arguments!')

	fileType = file[file.find('.') + 1:]
	fileName = file[:file.find('.')]
	print 'file type: ' + fileType
	print 'file name: ' + fileName

	try:
		stream = open(osp.join(repo.working_tree_dir, fileName + '.yml'), "r")
	except IOError:
		return make_response(jsonify({'error': 'Can not find file ' + str(file)}), 404)

	if(fileType == 'json'):
		print 'Return in json'
		return jsonify(yaml.load(stream))
	if(fileType == 'yml'):
		print 'Return in yaml'
		return yaml.dump(yaml.load(stream), default_flow_style=False, allow_unicode=True)

	return make_response({'Error':'Wrong return'}, 404)


def UpdateRepo(repoURL):
	# confirm or add .git to repo url
	if '.git' in repoURL:
		repoName = repoURL[repoURL.rfind("/") + 1 : -4]
	else:
		repoName = repoURL[repoURL.rfind("/") + 1 :]
		repoURL = repoURL + ".git"

	repoDir = osp.join(curDir, repoName)

	if(osp.exists(repoDir)):
		repo = PullRepo(repoURL, repoName)
	else:
		repo = CloneRepo(repoURL, repoName)

	return repo
	

def CloneRepo(repoURL, repoName):
	
	repo = Repo.clone_from(repoURL, repoName, branch='master')
	print 'Cloning repo'
	return repo


def PullRepo(repoURL, repoName):
	
	repo = Repo(osp.join(curDir, repoName))
	repo.remotes.origin.pull()
	print 'Repo already exist. Now pulling'
	return repo

if __name__ == "__main__":

	app.config['repoURL'] = sys.argv[1]
	app.run(debug=True,host='0.0.0.0')
	
