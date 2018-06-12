#add usr becoming server
import socket
import threading
import sys
import time
from random import randint

yPort = 48000
#yIPAdress = '127.0.0.1'



class Server:
    connections = []
    peers = []
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #run on localhost
        sock.bind(('127.0.0.1', yPort))
        sock.listen(1)

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            # allow close program while threads are running
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a)
            print(str(a[0]) + ":" + str(a[1]) + " connected")
            self.sendPeers()


    def handler (self, c, a):
        while True:
            #limit data to 1024 bytes
            data = c.recv(1024)
            # if no data sent, disconnect user
            # my impro
            if data == ('exit'):
                c.send(bytes("connection terminated\n"))
                self.connections.remove(c)
                self.peers.remove(a)
                c.close()
                self.sendPeers()
                print(str(a[0]) + ":" + str(a[1]) + " disconnected")
                # exit()
            else:
                #send beck data to connection
                for connection in self.connections:
                    if connection == c:
                        continue
                    #data can be sent only in bytes
                    connection.send(bytes(data))
                    #data = str(data).rstrip()

    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + str(peer) + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p))




class Client:
    def sendMsg(self, sock):
        while True:
            sock.send(bytes(raw_input("")))

    def __init__(self, adress):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((adress, yPort))

        ithread = threading.Thread(target=self.sendMsg, args=(sock, ))
        ithread.daemon = True
        ithread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11' :
                print("got peers " + data[1:])
            else:
                print str(bytes(data))

    # def updatePeers(self, peerData):
    #     p2p.peers = str(peerData, "utf-8").split(",")[:-1]



class p2p:
    names = []

    def addname( name):
        self.names.append(name)
        print (names[-1])

    def getname(self):
        print len(self.names)
        return self.names[-1]



# if more than one argument passed from command line, than do not start server
if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()

