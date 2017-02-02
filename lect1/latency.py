"""
Question:
Pick one IP from each region, find network latency from via the below code snippet
(ping 3 times), and finally sort regions by the average latency.
http://ec2-reachability.amazonaws.com/
Sample output:
1. us-west-1 [50.18.56.1] - Smallest average latency
2. xx-xxxx-x [xx.xx.xx.xx] - x
3. xx-xxxx-x [xx.xx.xx.xx] - x
...
15. xx-xxxx-x [xx.xx.xx.xx] - Largest average latency
"""
import subprocess
import os
import operator

"""
I created a file listing ips and their regions, like:
ap-northeast-2	52.78.0.0/16	52.78.63.252
ap-northeast-1	52.196.0.0/14	52.196.63.252
eu-west-2	52.56.0.0/16	52.56.34.0
...
"""
cwd=os.getcwd()
filename = cwd + "/testip.txt"
lines = [line.rstrip('\n') for line in open(filename)]
dic = {}
for line in lines:
	# extract ip and region names
	subline =  line.split("\t")
	region = subline[0] + " [" + subline[2] + "]"
	host = subline[2]

	ping = subprocess.Popen(
	    ["ping", "-c", "3", host],
	    stdout = subprocess.PIPE,
	    stderr = subprocess.PIPE
	)

	out, error = ping.communicate()
	# exract average latency from stdout and store into a dictionary
	avg = out[out.find(" = ") + 3:-3].split("/")[1]
	dic[region] = float(avg)

# sort dic base on average latency and print out one by one
num = 1
for item in sorted(dic.items(), key = operator.itemgetter(1)):
	print str(num) + ". " + item[0]
	num += 1

