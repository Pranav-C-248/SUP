import json
import socket

userSoc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
userSoc.connect(("192.168.1.3",8888))

data={
    "action":"register",
    "name":"ABC",
    "password":"123"
}

data=json.dumps(data)

userSoc.send(data.encode())

print(userSoc.recv(1024).decode())