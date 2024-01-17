import socket
import threading
import mysql.connector
import time

ip = "192.168.1.3"
port = 8888
names=[]
users=[]
nameToSocket={}
currentUser=None
loginStatus=False
registerStatus=False
isdbFree=True

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
    global isdbFree
    print(f"Executing {query}")
    time.sleep(2)
    while not isdbFree:
        print("Waiting...")
        time.sleep(5)
        
    else:
        isdbFree=False
        try:
            conn=mysql.connector.connect(host='localhost',database='sup',user='root',password='Drake@248')
            curs=conn.cursor(buffered=True)
            try:
                curs.execute(query)
                conn.commit()
                data=curs.fetchall()
                curs.close()
                conn.close()
                isdbFree=True
                return data
            except Exception as e:
                print("MySQL error ",e)
                curs.close()
                conn.close()
                isdbFree=True
                
        except:
            print("Fixing db...")
            conn=mysql.connector.connect(host='localhost',user='root',password='Drake@248')
            curs=conn.cursor(buffered=True)    
            curs.execute("create database if not exists sup")  
            print("Recreated db.")
            curs.execute("create table if not exists sup.users(id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL)")
            print("Recreated tables.")
            curs.close()
            conn.close()
            isdbFree=True
            return execdb(query)
        
        
def loginUser(userSocket,username,password):

    global loginStatus
    query = f"SELECT * FROM users WHERE username ='{username}' AND password = '{password}'"
    status=execdb(query)
    
    if status:
        userSocket.send("success".encode())
        loginStatus=True
    else:
        userSocket.send("fail".encode())
        loginStatus=False
        userSocket.close()
    print(loginStatus)
def registerUser(userSocket,username,password):
    global registerStatus
    query = f"INSERT INTO sup.users (username, password) VALUES ({username}, {password})"
    status=execdb(query)
    if status:
        userSocket.send("success".encode())
        registerStatus=True
    else:
        userSocket.send("fail".encode())
        registerStatus=False
        userSocket.close()    


def fetchFriendsList(userSocket,username):

    query=f"select * from friends where user1={username} or user2={username}"
    flist=execdb(query)
    if flist:
        #implement pickling/json logic here
        pass
    else:
        userSocket.send("null".encode())
        
def addFriend(userName,targetName):
    query=f"insert into friends (user1,user2,status) values ({userName},{targetName},pending)"
    execdb(query)
    #COMPLETE THIS
def removeFriend(userSocket,targetName):
    #COMPLETE THIS
    pass
def getSocket(username):
    #COMPLETE THIS
    pass

       
def accepter():
    while True:
        try:
            print("server is running")
            user,add=serverSock.accept()
            action,username,password=user.recv(1024).decode().split(",")
            if action=="login":
                loginUser(user,username,password)
            elif action=="register":

                registerUser(user,username,password)
            broadcast(f"{username} has joined the chat".encode())
            if loginStatus or registerStatus:
                users.append(user)
                names.append(username)
                thread=threading.Thread(target=messaging,args=(user,))
                thread.start()
            else:
                print("Wrong credentials")
                user.close()
                
            
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
    