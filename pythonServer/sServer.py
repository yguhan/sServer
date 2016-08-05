import socket
import threading
import SocketServer
import smtplib
import random

cctvIpToSocket = {}
userIpToSocket = {}

# real random number
authKey = ""

#key, (cctv Client, user Client)
keyToSockets = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
#        while(True):
        data = self.request.recv(1024)
        print "client joined !!"
        print "Address : ", self.client_address
        print "Request : ", self.request
#            cctvIpToSocket[self.client_address]=self.request
#            keyToSockets[authenticationKey]=self.request

#   cctv side protocol :1, user side protocol :0
        if(data != None):
            print "protocol & contents: ", data
            
            #USER
            if(data[0] == '0'):
                userClient(self, data)

            #CCTV
            elif(data[0] == '1'):
                cctvClient(self, data)
            else:
                print "protocol format does not exist"

"""
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
    authKey = str(random.randrange(1000, 10000))
    keyToSockets[authKey] = (client, None)
    cctvIpToSocket[client.client_address] = client


    def sendingMail(data, authKey):

        email_receiver = data[2:].split('\n')[0]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("postechserver@gmail.com", "wjswkghlfh")

        server.sendmail("postechserver@gmail.com", email_receiver, authKey)
        print "send email to {}".format(data[2:])

        server.quit()

    sendingMail(data, authKey)


    while(True):
        data = client.request.recv(1024)
        if(data!=None):
            if(keyToSockets[authKey][1]!= None ):

                if(data[1] == '0'):
                    print "cctv protocol ", data[0:1]
                    print "msg cctv>>user ", data[2:]

                elif(data[1] == '1'):
                    print "cctv protocol ", data[0:1]
                    print "img cctv>>user "
                keyToSockets[authKey][1].request.sendall(data[2:])
                data = None

            else:
                print "{} of USER does not match ".format(client.client_address)
                data = None

def userClient(client, data):

    key = data[1:].split('\n')[0]
    data = None
    print "authKey: ", authKey
    print "key: ", key
    print "keyToSockets"
    print keyToSockets

    if(keyToSockets[key] != None):
        keyToSockets[key] = (keyToSockets[key][0] , client)
        userIpToSocket[client.client_address] = client

        while(True):
            data = client.request.recv(1024)
            if(data!=None):
                print "user protocol ", data[0]
                print "user>>cctv: ",data[1:]
                keyToSockets[key][0].request.sendall(data[1:])
                data = None

    else:
        print "{} of CCTV does not match ".format(client.client_address)
        data = None

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "ubuntu.poapper.com", 3600

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

