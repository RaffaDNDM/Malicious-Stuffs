#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import socket, threading
from termcolor import cprint

def manage_info(client_sd, client_address):
    '''
    Manage remote client request.

    Args:
        client_sd (socket.socket): Socket descriptor for the 
                                   remote client

        client_address (tuple): Tuple (IP_address, port), where:
                                IP_address: IP address of the client
                                port: Port number
    '''
    
    #Read the size of the message
    size = ''
    while True:
        size += client_sd.recv(1).decode()

        if size[-2:] == '\r\n':
            size = size[:-2]
            break

    #Read the message with length of size bytes    
    msg = client_sd.recv(int(size)).decode()
    #Print the directory and its content (received from the client) 
    cwd, subfolders = msg.split('\r\n')
    subfolders_list = subfolders.split(',')

    cprint(f'\n{cwd}', 'yellow')
    for fold in subfolders_list:
        print(f'\t{fold}')

def main():
    IP_address = '127.0.0.1'
    PORT = 8080

    try:
        #Create TCP socket
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Bind the server to the specified address
        sd.bind((IP_address, PORT))
        #Listen queue
        sd.listen(10)
    except socket.error:
        print('Something goes wrong')
        exit()

    while True:
        #Receive a connection request from a client
        client_sd, client_address = sd.accept()
        #Manage the requests of the client through a thread
        t = threading.Thread(target=manage_info, args=(client_sd, client_address))
        t.start()

if __name__=='__main__':
    main()