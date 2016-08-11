import socket
import threading
import SocketServer
import smtplib
import random

cctvIpToSocket = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
#        while(True):
        print "client joined !!"
        print "Address : ", self.client_address
        print "Request : ", self.request
        cctvIpToSocket[self.client_address]=self.request
#        keyToSockets[authenticationKey]=self.request
        
        data = self.request.recv(1024)
#   cctv side protocol :1, user side protocol :0
        if(len(data)!=0):
            print "protocol & contents: ", data
            #cctvClient(self, data)

            #CCTV
            if(data[0] == '1'):
                cctvClient(self, data)

            #cctvClient(self, data)
"""
            else:
                print "protocol format does not exist"

            cur_thread = threading.current_thread()
            response = "{}: {}".format(cur_thread.name, data)
            self.request.sendall(response)
            print "server received: ", data
            data = None
"""

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def cctvClient(client, data):
    print "cctv start"
    #authKey = str(random.randrange(1000, 10000))
    keyToSockets[authKey] = (client, None)
    cctvIpToSocket[client.client_address] = client

    while(True):
        data = client.request.recv(1024)
         
        
        if(data!= None):
 
            if(data[0:2] == '10'):
                #print /"cctv protocol ", data[0:1]
                #print "msg cctv>>user ", data[2:]
                print "msg cctv >> user: ", data
                data = None
            
            else: 
                f=open('find.txt', 'a')
                contents = ""
                for x in data:
                    if(x != None):
                        contents += x
                        #print x
                try:
                    if(len(contents) >0):
                        print contents
                        f.write(contents)
                except IOError as (er, strer):
                    print "I/O er({0}): {1}".format(er, strer)
                
                data = None
                f.close()
            


            """
            elif(data[0:2] == '11'):
                #data = client.request.recv(1024)
                #jpgSize = int(data)
                #print "jpg size: ", jpgSize
                
                #print "img size : ", data
                
                print "#s from cctv >> user" (data[2:])
                data = None
                
                while(True):
                    data = client.request.recv(1024)
                    #f.write(data)
                    if(data != None):
                        
                        try:
                            if(data[0:2]=='12'):
                                print "image transfer is done"
                                data = None
                                break
                            else:
                                if(keyToSockets[authKey][1] != None):
                                    keyToSockets[authKey][1].request.sendall(data)
                                    data = None
                                else:
                                    print "user Socket is disconnected"
                                    data = None
                        except:
                            print "protocol error"

                #print "img cctv>>user ", data
              
                print "success:reading image file "
                            
            data = None
            """

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "172.31.4.200", 8000
   
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address


    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server running "

    server.serve_forever()

