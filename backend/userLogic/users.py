import socket
import threading

class user:
    
    def __init__(self,name) -> None:
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


                    
                

