import socket
import threading
import sys

yPort = 30000
#yIPAdress = '127.0.0.1'

class Server:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        #run on localhost
        self.sock.bind(('127.0.0.1', yPort))
        self.sock.listen(1)


    def handler (self, c, a):
        while True:
            #limit data to 1024 bytes
            data = c.recv(1024)
            #send beck data to connection
            for connection in self.connections:
                #data can be sent only in bytes
                connection.send(bytes(data))
                connection.send(bytes("\n"))
                data = str(data).rstrip()
                #my impro
                if data == ('exit'):
                    connection.send(bytes("connection terminated\n"))
                    self.connections.remove(c)
                    c.close()
                    exit()
            if not data:
                print(str(a[0]) + ":" + str(a[1]) + " disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            # allow close program while threads are running
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ":" + str(a[1]) + " connected")

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            iput = input("write message: ")
            iput = str(iput).rstrip()
            self.sock.send(bytes(iput))

    def __init__(self, adress):
        self.sock.connect((adress, yPort))

        ithread = threading.Thread(target=self.sendMsg)
        ithread.daemon = True
        ithread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(data)

# if more than one argument passed from command line, than do not start server
if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()


