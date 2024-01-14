import socket
import threading
import mysql.connector
import time

ip = "192.168.1.3"
port = 8888
names=[]
users=[]
loginStatus=False
registerStatus=False
dbFree=True

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((ip, port))

serverSock.listen()
serverSock.settimeout(2)
print("server is listening...")

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
        
def execdb(query):
    global dbFree
    while not dbFree:
        time.sleep(0.2)
        
    else:
        dbFree=False
        try:
            conn=mysql.connector.connect(host='localhost',database='sup',user='root',password='Drake@248')
            curs=conn.cursor()
            try:
                curs.execute(query)
                conn.commit()
                data=curs.fetchall()
                curs.close()
                conn.close()
                dbFree=True
                return data
            except Exception as e:
                print("MySQL error ",e)
                curs.close()
                conn.close()
                dbFree=True
                
        except:
            print("Fixing db...")
            conn=mysql.connector.connect(host='localhost',user='root',password='Drake@248')
            curs=conn.cursor()    
            curs.execute("create database if not exists sup")  
            print("Recreated db.")
            curs.execute("create table if not exists sup.users(id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL)")
            print("Recreated tables.")
            curs.close()
            conn.close()
            dbFree=True
            return execdb(query)
        
        
def loginUser(userSocket,username,password):
    global loginStatus
    query = f"SELECT * FROM users WHERE username ={username} AND password = {password}"
    status=execdb(query)
    if status:
        userSocket.send("success".encode())
        loginStatus=True
    else:
        userSocket.send("fail".encode())
        loginStatus=False
def registerUser(userSocket,username,password):
    global registerStatus
    query = f"INSERT INTO users (username, password) VALUES ({username}, {password})"
    status=execdb(query)
    userSocket.send("success".encode())
    registerStatus=True
        
        
def accepter():
    while True:
        try:
            user,add=serverSock.accept()
            action,username,password=user.recv(1024).decode().split(",")
            if action=="login":
                loginUser(user,username,password)
            elif action=="register":
                registerUser(user,username,password)
            users.append(user)
            # user.send("NAME".encode())
            # name=user.recv(1024).decode()
            names.append(username)
            broadcast(f"{username} has joined the chat".encode())
            if loginStatus or registerStatus:
                thread=threading.Thread(target=messaging,args=(user,))
                thread.start()
            else:
                break
        except TimeoutError:
            continue
        except KeyboardInterrupt:
            print("CLOSED")
            break   
            
t=threading.Thread(target=accepter,daemon=True)
t.start()
while True:
    try:
        time.sleep(5)
    except:
        break
    