import socket
import threading
import time
import sys

# host_name = socket.gethostname()
# server_address = socket.gethostbyname(host_name)

server_ip = "127.0.0.1" 
server_port = 5111 

clients = []

########################################################################

def connectionAccept(s):
    try:
        c,addr = s.accept() #c,the connected socket object
    except:
        return
    username = c.recv(1024).decode('utf-8')
    print(f"{username} connected from this address:{addr}")
    
    messageForJoiner = f"Hello {username} You have connected from this address: {addr}"
    c.send(messageForJoiner.encode('utf-8')) #Information for the newly connected client
        
    clients.append([c,addr,username])
    
    messageForOthers = f"{username} joined the chat!"
    for i in clients: #Inform the users in the chatroom about the new user
        if i[0] != c:
            i[0].send(messageForOthers.encode('utf-8'))
            
    #Start a new thread for the new client
    thread = threading.Thread(target=clientHandler, args=(c,username,s,),daemon=True)
    thread.start()
    
    
    
####################################################################   

def clientHandler(c,username,s):
   flag = True 
   while flag:
       try:
           message = c.recv(1024).decode('utf-8')
           
           if message == "": #Check if the new message is empty
               continue
           elif message:
               try:
                   for i in clients: #Sends the incoming message to other users
                       if i[0] != c:
                           messageFormatted = (f"{username}> {message}")
                           i[0].send(messageFormatted.encode('utf-8'))
                          
                   print(f"{username} sent this message:{message}")
               except: #Checking if the message was successfully sent to other users
                   flag = False
                   break
           else:
               flag = False
               break
               
       except: #Incoming
           flag = False
           break
       
   for i in clients:
       if i[0] == c:
           clients.remove(i)
   c.close()
   print(f"{username} left")
   
   message = f"{username} left the chat!"
   for i in clients:
       i[0].send(message.encode('utf-8'))
   if len(clients) == 0: 
       serverClose(s)
   
   return 
       

#################################################################################

def serverStart():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        print("Socket created")
    
        s.bind((server_ip,server_port))
        print(f"Socket is open on {server_port}")
    
        s.listen(20) #Allowed connection number
        print("Socket is listening")
    except:
        print("There was a error while trying to open or bind the socket")
        serverClose(s)
    
    while True:#Even tho the program gets the cient 0 massage and starts the closing process this while loop doesn't close.
        connectionAccept(s)
        if len(clients) == 0:
           break
    serverClose(s)
           
###################################################################################

def serverClose(s):
    
    for i in threading.enumerate():
        print(i)
    
    print("Connected clients:")
    if len(clients) > 0:
        for i in clients:
            print(i)
            i[0].close()
            clients.remove(i)
    #Close the socket
    s.close()
    print("Open sockets are closed ,closing the server")
  
    time.sleep(2)
    
    sys.exit(0)

##########################################################################################
serverStart()


