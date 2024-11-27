from socket import *

def main():
    # Create a UDP socket
    serverSock = socket(AF_INET, SOCK_DGRAM)

    # Initialize server address
    serverAddress = ('127.0.0.1', 20000)
    
    # Bind the socket to the address
    try:
        serverSock.bind(serverAddress)
    except Exception as e:
        print("Bind error:", e)
        serverSock.close()
        return

    BUFFER_SIZE = 65507
    print("Server is ready and waiting for messages at UDP port 20000")
    addressToName = {}
    nameToAddress = {}


    def message_all(message, serverSock, clientAddress):
        for name, address in nameToAddress.items():
            if address == clientAddress:
                continue
            serverSock.sendto(message.encode(), address)
        

    def find_targets(word, names):
        message = ''
        for idx in range(1, len(word)):
            if word[idx] == 'msg':
                message = word[idx+1:]
                message = " ".join(message)
                break
            names.append(word[idx])
        return message
        

    def send_messages(message, names,serverSock, missing_names):
        for name in names:
            if name not in nameToAddress:
                missing_names.append(name)
            else:
                serverSock.sendto(message.encode(), nameToAddress[name])
        return missing_names


    def do_something(word, clientAddress, serverSock, sender):
        if word == 'users':
            
            all_curr_users = []
            for address,names in addressToName.items():
                all_curr_users.append(names)
            all_curr_users = ' '.join(all_curr_users)
            return "All Users: " + all_curr_users
        
        if word == 'leave':
            print(addressToName[clientAddress],' has left the chat')
            del nameToAddress[addressToName[clientAddress]]
            del addressToName[clientAddress]
            return 'Bye ...'
        
        word = word.split(' ')
        names = []
        if word[0] == 'to':
            message = find_targets(word, names)
            message = sender + ": <" + message  + ' >'
            if 'all' in names:
                message_all(message, serverSock, clientAddress)
            else:
                missing_names = send_messages(message, names, serverSock, missing_names = [])
                if missing_names:
                    missing_names_string = " ,".join(missing_names)
                    return 'ERROR MESSAGE: < ' + missing_names_string + ' > ARE NOT ONLINE! ' 
            return "Message Delivered!"
        else:
            return "Error, Command May Be Incorrect"
        
        
    while True:
        try:
            # Receive message from client
            data, clientAddress = serverSock.recvfrom(BUFFER_SIZE)
            word = data.decode()
            word = word.strip()
            if not data:
                break
            if clientAddress not in addressToName:
                # address --> senderName
                # senderName --> address
                addressToName[clientAddress] = word
                nameToAddress[word] = clientAddress
                
                print(addressToName[clientAddress], ' has joined the chat ')
                new_message = 'Welcome'
            else:
                sender = addressToName[clientAddress]
                new_message = do_something(word, clientAddress, serverSock, sender)
            if new_message != '':
                serverSock.sendto(new_message.encode(), clientAddress)

            
        
        except Exception as e:
            print("Error receiving from client:", e)
            break

    serverSock.close()

if __name__ == "__main__":

    main()
