import socket                
import threading
import time
import sys

host = "127.0.0.1"
port = 5111    

##############################################         
def getMessage(s):
    
    while True:
        try:
            message = s.recv(1024)
        
            if message != 0:
                print(message.decode('utf-8'))
            else:
                s.close()
                return
        
        except:
            s.close
            return
##################################################
     
def clientStart():
    
    # Create the socket object
    s = socket.socket()    
    
    username = input("Enter your username:")   
    
    try:
        # Bağlantıyı yap
        
        s.connect((host, port)) 
        
        s.send(username.encode('utf-8'))
        
        # serverden yanıtı al
        answer = s.recv(1024)
        print(answer.decode('utf-8'))
        
        thread = threading.Thread(target=getMessage, args=(s,))
        thread.start()
        
        while True:
            message = input()
            
            s.send(message.encode('utf-8'))
        
    except:
        print("Server is not online.")
        s.close()
    
    time.sleep(2)
    sys.exit(0)
    
  
clientStart()