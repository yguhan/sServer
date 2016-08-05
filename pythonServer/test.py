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

allSockets = []

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
#        while(True):
        data = self.request.recv(1024)
        print "client joined !!"
        print "Address : ", self.client_address
        print "Request : ", self.request
#        cctvIpToSocket[self.client_address]=self.request
#        keyToSockets[authenticationKey]=self.request

#   cctv side protocol :1, user side protocol :0
        if(data != None):
            #print "protocol & contents: ", data
            allSockets.append(self)
            cctvClient(self, data)

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

#    sendingMail(data, authKey)

    f = open('dataRecv.txt', 'w')
    while(True):
        
        data = client.request.recv(1024)
        #print "direct-data: ", data   
        if(data != None or data != ' '):
            f.write(data)
            print "write on the screen: ", data
            #print data
        
        data = None
        #f.write(data)
#        data = None

        """
        if(data[0]!=None and data[1]!=None):
 
            if(data[1] == '0'):
                #print /"cctv protocol ", data[0:1]
                #print "msg cctv>>user ", data[2:]
                print "msg cctv >> user: ", data

            elif(data[0:1] == '11'):
                data = None
                data = client.request.recv(1024)
                jpgSize = int(data)
                print "jpg size: ", jpgSize
                
                #print "img size : ", data
                
                f = open('cctvImg.txt', 'w')
               
                while(True):
                    data = client.request.recv(1024)
                    f.write(data)
                    if(len(data) > 1):
                        if(data[0:1]=='12'):
                            break
                #print "img cctv>>user ", data
               
                while(jpgSize > 0):
                    data = client.request.recv(1024)
                    f.write(data)
                    jpgSize = jpgSize-int(data)
               
                print "success:reading image file "
                f.close()
            data = None
        """
#        jpgSize = data
#       if(data[1] != '0'):
#          print "jpg size: ", data
    f.close()

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
    HOST, PORT = "ubuntu.poapper.com", 3700

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

