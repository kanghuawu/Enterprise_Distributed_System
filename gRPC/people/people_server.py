from concurrent import futures
import time
import math
import grpc
import people_pb2
import people_pb2_grpc
import people_resources

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def get_info(people_db, name):
  for people in people_db:
    if people.name == name:
      return people
  return None

class PeopleSearchServicer(people_pb2_grpc.PeopleSearchServicer):
  def __init__(self):
    self.db = people_resources.people_database()

  def FindByFullName(self, request, context):
  	info = get_info(self.db, request)
  	if info is None:
  		return people_pb2.PeopleInfo(name = "", number = "", company = "")
  	else:
  		return info
  def FindByFirstCharacter(self, request, context):
    for people in self.db:
      if request.name[0] == people.name.name[0]:
        yield people

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  people_pb2_grpc.add_PeopleSearchServicer_to_server(PeopleSearchServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()