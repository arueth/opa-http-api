package httpapi.authz

car_owner = {"id1234": "alice", "id2345": "alice" , "id3456": "ricardo"}
employees = ["alice", "eve", "ricardo", "carmen"]

import input as http_api

# http_api = {
#   "method": "GET"
#   "path": ["v1", "cars", "id1234"],
#   "user": "alice"
# }

default allow = false

allow {
  http_api.method == "POST"
  http_api.path == ["v1", "cars"]
  employees[_] == http_api.user
}

allow {
  http_api.method == "GET"
  http_api.path == ["v1", "cars", id]
}

allow {
  http_api.method == "PUT"
  http_api.path == ["v1", "cars", id]
  employees[_] == http_api.user
}

allow {
  http_api.method == "DELETE"
  http_api.path == ["v1", "cars", id]
  car_owner[id] == http_api.user
}
