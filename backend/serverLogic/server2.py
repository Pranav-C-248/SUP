import socket
import threading
import mysql.connector
import time
import json
from dotenv import dotenv_values

config=dotenv_values(".env")
IP = config.get('IP')
PORT = config.get('PORT')
PORT=int(PORT)
DBHOST = config.get('DBHOST')
DBNAME = config.get('DBNAME')
DBUSER = config.get('DBUSER')
DBPASS = config.get('DBPASS')


class User:
    def __init__(self,socket,name) -> None:
        self.name=name
        self.socket=socket
        self.loginState=False
        

isdbFree=True

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((IP, PORT))

serverSock.listen()
serverSock.settimeout(2)
print("server is listening...")
        
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
            conn=mysql.connector.connect(host=DBHOST,database=DBNAME,user=DBUSER,password=DBPASS)
            curs=conn.cursor(buffered=True)
            try:
                if query[:6]=="INSERT":
                    curs.execute(query)
                    if curs.rowcount>0:
                        conn.commit()
                        curs.close()
                        conn.close()
                        return "success"
                    else:
                        return "fail"
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
            conn=mysql.connector.connect(host=DBHOST,user=DBUSER,password=DBPASS)
            curs=conn.cursor(buffered=True)    
            curs.execute(f"create database if not exists {DBNAME}")  
            print("Recreated db.")
            curs.execute(f"create table if not exists {DBNAME}.users(id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL)")
            print("Recreated tables.")
            curs.close()
            conn.close()
            isdbFree=True
            return execdb(query)
        
        
def loginUser(user,password):
    query = f"SELECT * FROM users WHERE username ='{user.name}' AND password = '{password}'"
    status=execdb(query)
    print("Status: ",status)
    if status:
        user.socket.send("success".encode())
        user.loginState=True
    else:
        user.socket.send("fail".encode())
        user.loginState=False
        user.socket.close()
    print(user.loginState)
    
def registerUser(user,password):
    query = f"INSERT INTO users (username, password) VALUES ('{user.name}', '{password}')"
    status=execdb(query)
    if status=="success":
        user.socket.send("success".encode())
        print("Registered")
    else:
        user.socket.send("fail".encode())
        user.socket.close()    


def fetchFriendsList(user):

    query=f"select * from friends where user1='{user.name}'"
    flist=execdb(query)
    if flist:
        flist=json.dumps()
        user.socket.send(flist)
        print("Friends: ",flist)
    else:
        print("No friends :( ")
        user.socket.send("null".encode())
        
def addFriend(userName,targetName):
    query=f"insert into friends (user1,user2,status) values ({userName},{targetName},pending)"
    query1=f"insert into friends (user1,user2,status) values ({targetName},{userName},pending)"
    execdb(query)
    execdb(query1)
    #COMPLETE THIS
def removeFriend(userSocket,targetName):
    #COMPLETE THIS
    pass

def message2frnd(targetUser,text:str):
   pass
       
def accepter():
    while True:
        try:
            userSock, address= serverSock.accept()
            data=userSock.recv(1024).decode()
            data=json.loads(data)   
            user=User(userSock,data["name"])
            
            if data["action"]=="login":
                loginUser(user,data["password"])
            elif data["action"]=="register":
                registerUser(user,data["password"])
            elif data["action"]=="text":
                if user.loginState is True:
                    message2frnd(data["target"],data["content"])
            elif data["action"]=="fetch":
                if user.loginState is True:
                    fetchFriendsList(user.name)
 
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
        print("Closing......")
        break
    