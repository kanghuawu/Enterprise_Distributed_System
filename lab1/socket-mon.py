import psutil
import pandas
import json

def AddrPort(tup):
	return "@".join(str(x) for x in tup)

# Collect all TCP sockets connections
data = []
for con in psutil.net_connections(kind='tcp'):
	if con.laddr and con.raddr:
		data.append({'pid': con.pid, 'laddr': AddrPort(con.laddr), 'raddr': AddrPort(con.raddr), 'status': con.status})
col = ['pid', 'laddr', 'raddr', 'status']
df = pandas.DataFrame(data, columns = col)


# Group by pid and sort by pid's count
group = df.groupby('pid')
df['count'] = group['laddr'].transform('count')
df.sort(['count', 'pid'], ascending = [False, False], inplace = True)

# export to csv file
df[col].to_csv('output.csv', index = False)

