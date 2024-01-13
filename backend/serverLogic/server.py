import socket
import threading
import mysql.connector
import signal
import sys
import socket

# Flag to indicate whether the server should continue running
running = True

# Signal handler to set the running flag to False on Ctrl+C
def signal_handler(sig, frame):
    global running
    print('Ctrl+C pressed, terminating server...')
    running = False

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

ip = "192.168.1.3"
port = 8888

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((ip, port))

serverSock.listen()
print("server is listening...")

users = []
names = []
running = True


def broadcast(message):
    for user in users:
        user.send(message.encode())


def usermsg(user):
    try:
        msg = user.recv(1024)
        broadcast(f"{msg}")
    except Exception:
        i = users.index(user)
        users.remove(user)
        broadcast(f"{names[i]} has left the chat")


def receive():
    global running
    try:
        while running:
            user, add = serverSock.accept()
            users.append(user)
            user.send("NAME".encode())
            name = user.recv(1024).decode()
            names.append(name)
            broadcast(f"{name} has joined the chat")
            thread = threading.Thread(target=usermsg, args=(user,))
            thread.start()
        
        
    except KeyboardInterrupt:
        print("ended")
        exit(0)
        
receive()
