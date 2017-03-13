from flask import Flask
import requests
import sys

app = Flask(__name__)

@app.route("/")

def hello():
	if(len(sys.argv) == 1):
	    return "Need to pass third argument"
	else:
		r = requests.get('https://raw.githubusercontent.com/sithu/assignment1-config-example/master/dev-config.yml')
		return r.content

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
