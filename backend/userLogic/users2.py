import eel 
import socket
import threading


#global variables
loginStatus=False
username=None


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
        listenThread=threading.Thread(target=self.listen)
        listenThread.start()
        writeThread=threading.Thread(target=self.write)
        writeThread.start()



eel.init("frontend")
curUser=user()
@eel.expose
def loginHandle(uName,uPass):
    global loginStatus,username,curUser
    curUser.name=uName
    action="login"
    curUser.userSoc.send(f"{action},{uName},{uPass}".encode())
    loginstate=loginSocket.recv(1024).decode()
    if loginstate is True:
        loginStatus=True
        username=uName
        return loginStatus
    else:
        loginStatus=False
        return loginStatus

if loginStatus is True:
    user=user(username)
    user.start()

try:
    eel.start('login.html', size=(700, 500), mode='chrome', port=0)
except (SystemExit, MemoryError, KeyboardInterrupt):
    # Handle exceptions when the Eel application is closed
    pass
except Exception as e:
    # Print other exceptions for troubleshooting
    print(f"Error: {e}")