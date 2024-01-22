import json


data={
    "action":"login",
    "name":"Drake",
    "password":"123"
}

data=json.dumps(data)
data=json.JSONDecoder
print(type(data))