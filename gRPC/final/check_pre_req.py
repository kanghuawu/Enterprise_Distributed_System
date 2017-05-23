"""
Check whether DB server is up and a client can access to it.
"""
import sys
import hrw
from client import DBClient
import uuid

class DBCheck(object):

    def __init__(self):
        self.client = None
        node1 = '0.0.0.1:3000'
        node2 = '0.0.0.1:4000'
        node3 = '0.0.0.1:5000'
        self.ring = hrw.Ring()
        self.ring.add(node1)
        self.ring.add(node2)
        self.ring.add(node3)

    def put(self):
        print "########## Put ###########"
        key = uuid.uuid4().hex
        node = self.ring.hash(key)
        print "storing at", node
        self.setupDB(node[-4:])
        user = {
            'id' : key,
            'name': 'Foo Bar',
            'email': 'foo_bar@gmail.com'
        }
        print "Put Request:\n", user
        resp = self.client.put(user)
        print "Put Response:\n%s" % resp
        return resp.id
        

    def get(self, id=None):
        print "########## Get ###########"
        resp = self.client.get(id)
        print "Get Response:\n%s" % resp


    def info(self):
        print "########## Info ###########"
        resp = self.client.info()
        print "Info Response:\n%s" %resp    

    def setupDB(self, port):
        self.client = DBClient(host='0.0.0.0', port=int(port))

if __name__ == '__main__':
    # total = len(sys.argv)
    # if total < 2:
    #     print "Usage: python check_pre_req.py {SERVER_PORT}"
    #     sys.exit(0)
    
    # port = int(sys.argv[1])
    db = DBCheck()
    id = db.put()
    db.get(id)
    db.info()