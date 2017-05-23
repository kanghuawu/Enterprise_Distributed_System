from __future__ import print_function

import random
import time

import grpc

import people_pb2
import people_pb2_grpc


def findFullName(stub):
  people_info = stub.FindByFullName(people_pb2.Name(name = "Jennifer"))
  print(people_info.name)

def findByFirstChar(stub):
  people_infos = stub.FindByFirstCharacter(people_pb2.Name(name = "Jennifer"))
  for people in people_infos:
  	print(people)
  	time.sleep(1)

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = people_pb2_grpc.PeopleSearchStub(channel)
  print("-------------- FindByFullName --------------")
  findFullName(stub)
  print("-------------- ListFeatures --------------")
  findByFirstChar(stub)


if __name__ == '__main__':
  run()
