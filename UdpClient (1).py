# This code will in Windows
from socket import *
from select import select
import sys
import os
import msvcrt

PORT = 20000
BUFFER_SIZE = 65507

buffer = []
def checkKeyboardInput():
    if os.name == 'nt':  # Windows
        import msvcrt
        if msvcrt.kbhit():
            ch = msvcrt.getwch()  # Get a single character from the input
            print(ch, end='', flush=True)
            if ch == '\r':
                print(flush=True)
                line = "".join(buffer)
                buffer.clear()
                return line            
            elif ch == '\b':
                if len(buffer) > 0:
                    buffer.pop()
                    line = "".join(buffer)
                    print(f"\b  ", end='', flush=True)
                    print(f"\r{line}", end='', flush=True)
            else:
                buffer.append(ch)
                return None

def main():
    # Create UDP socket for port PORT1
    clientSock = socket(AF_INET, SOCK_DGRAM)
    peer = ('127.0.0.1', 20000)

    print("Server is ready and waiting for messages at UDP port 20000")

    while True:
        # 0.05 second timeout
        rset, _, _ = select([clientSock], [], [], 0.05)  

        for sock in rset:
            data, peer = sock.recvfrom(BUFFER_SIZE)
            if sock is clientSock:
                print(data.decode())
                if data == 'Bye ...':
                    clientSock.close()


        line = checkKeyboardInput()
        if line is not None:
            try:
                clientSock.sendto(line.encode(), peer) 
            except Exception as e:
                print("Problem sending packet to the peer:", e)
                continue
           

if __name__ == "__main__":

    main()









"""
from socket import *
from select import select
import sys
import os

BUFFER_SIZE = 65507

def main():
    # Create a UDP socket
    clientSock = socket(AF_INET, SOCK_DGRAM)
    
    # Get the server IP address from the user
    destIP = '127.0.0.1'
    # Initialize server address
    peer = (destIP, 20000)
    
    while True:

        msg = input(">>> ")
        
        
        # Send the message to the server
        try:
            clientSock.sendto(msg.encode(), peer)
        except Exception as e:
            print("Problem sending packet to the peer:", e)
            continue
                

        # Wait for the server to reply
        try:
            data, server = clientSock.recvfrom(BUFFER_SIZE)
            print(data.decode())
        except Exception as e:
            print("Error receiving from server. Server not running?", e)
        if msg == "leave":
            break
        
    clientSock.close()

if __name__ == "__main__":
    main()"""