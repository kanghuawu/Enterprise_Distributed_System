"""
################################## client.py #############################
# DBClient, a GRPC client, to communicate to the DB Service.
################################## client.py #############################
"""
import grpc
import db_pb2
import hrw

class DBClient(object):
    
    def __init__(self, host='0.0.0.0', port=3000):
        _channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = db_pb2.DBStub(channel=_channel)
        print "Client connected to %s:%d" % (host, port)
        node1 = '127.0.0.1:3000'
        node2 = '127.0.0.1:4000'
        node3 = '127.0.0.1:5000'
        self.ring = hrw.Ring()
        self.ring.add(node1)
        self.ring.add(node2)
        self.ring.add(node3)

    def info(self):
        return self.stub.info(db_pb2.Empty())


    def put(self, kv):
        _data = db_pb2.Data(entry=kv)
        req = db_pb2.PutRequest(data=_data)
        return self.stub.put(req)


    def get(self, _id):
        req = db_pb2.GetRequest(id=_id)
        return self.stub.get(req)
