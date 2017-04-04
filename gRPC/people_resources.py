import json
import people_pb2


def  people_database():
  people_info_list = []
  with open("people_db.json") as people_db_file:
    for item in json.load(people_db_file):
      people_info = people_pb2.PeopleInfo(
        name = people_pb2.Name(name = item["name"]), 
        num = people_pb2.Number(num = item["number"]),
        company = people_pb2.Company(company = item["company"]))
      people_info_list.append(people_info)
  return people_info_list

if __name__ == '__main__':
  run()