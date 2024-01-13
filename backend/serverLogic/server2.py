import socket
import threading

ip = "192.168.1.3"
port = 8888

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((ip, port))

serverSock.listen()
print("server is listening...")

names=[]
users=[]

def broadcast(msg):
    for user in users:
        user.send(msg)
        
def messaging(user):
    while True:
        try:
            # Broadcasting Messages
            message = user.recv(1024).decode()
            broadcast(message.encode())
        except:
            # Removing And Closing Clients
            index = users.index(user)
            users.remove(user)
            user.close()
            nickname = names[index]
            broadcast(f'{nickname} left!'.encode())
            names.remove(nickname)
            break
def accepter():
    while True:
        user,add=serverSock.accept()
        users.append(user)
        user.send("NAME".encode())
        name=user.recv(1024).decode()
        names.append(name)
        broadcast(f"{name} has joined the chat".encode())
        thread=threading.Thread(target=messaging,args=(user,))
        thread.start()
        
accepter()
    