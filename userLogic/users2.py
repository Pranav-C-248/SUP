import eel 
import socket
import json
#global variables
loginStatus=False


class user:
    def __init__(self,name=None) -> None:
        self.name=name
        self.userSoc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.userSoc.connect(("192.168.1.3",8888))
        
    def listen(self):
        while True:
            try:
                msg=self.userSoc.recv(1024).decode()
                if msg=="NAME":
                 self.userSoc.send(self.name.encode())
                else:
                    print(msg)
            except KeyboardInterrupt:
                print("Error occured")
                self.userSoc.close()
                break
    def write(self):
        while True:
            try:
                msg=f"{self.name}: {input('')}".encode()
                self.userSoc.send(msg)
            except:
                print("Error occured")
                self.userSoc.close()

    def start(self):
        print("Socket starting...")
        eel.spawn(function=self.listen)
        eel.spawn(function=self.write)


eel.init("gui")
curUser=user()


@eel.expose
def loginHandle(uName,uPass):
    global loginStatus,curUser
    curUser.name=uName
    
    package={
        "action":"login",
        "name":f"{uName}",
        "password":f"{uPass}"
    }
    
    package=json.dumps(package)
    curUser.userSoc.send(package.encode())

    loginstate=curUser.userSoc.recv(1024).decode()
    
    if loginstate == "success":
        loginStatus=True
        print(loginStatus)
        
        # curUser.start()
        return loginStatus
    else:
        print("Wrong creds")
        loginStatus=False
        return loginStatus
        

try:
    eel.start('login.html', size=(700, 500), mode='chrome', port=0)
except :
    print("Closing app...")
