#######################
# @author: RaffaDNDM
# @date:   2023-01-17
#######################

from Crypto.Cipher import AES
from Crypto import Random
import os
from termcolor import cprint, colored
import shutil
import customtkinter
import hashlib
import pyotp
import qrcode
from tkinter import messagebox
import base64

class CipherData:
    '''
    AES cipher/decipher of files inside a folder.

    Args:
        otp_key (str): Key to be used for Authenticator

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

    DEFAULT_PATH = 'dat/'
    FILE_LIST = []
    DIR_LIST = []
    CHECK_ENCRYPTED = b'ENCRYPTED'

    def __init__(self, otp_key):
        self.master = customtkinter.CTk()
        self.master.protocol("WM_DELETE_WINDOW", self.master.quit())
        self.master.geometry('450x120')
        
        self.totp = pyotp.TOTP(otp_key)
        self.OTP_counter = 0

        PAD_UNIT=0.025
        COMP_FULLSIZE_X = 1-4*PAD_UNIT
        COMP_FULLSIZE_Y = 1-20*PAD_UNIT

        customtkinter.CTkLabel(self.master, text="Folder", justify='right', anchor='e').place(relx=PAD_UNIT, rely=2*PAD_UNIT, relwidth=COMP_FULLSIZE_X*0.15, relheight=COMP_FULLSIZE_Y*0.25)
        self.path_comp = customtkinter.CTkEntry(self.master)
        self.path_comp.insert(10, "")
        self.path_comp.place(relx=2*PAD_UNIT+COMP_FULLSIZE_X*0.15, rely=2*PAD_UNIT, relwidth=COMP_FULLSIZE_X*0.7, relheight=COMP_FULLSIZE_Y*0.25)
        customtkinter.CTkButton(self.master, text='Select', command=self.choose_dir).place(relx=3*PAD_UNIT+COMP_FULLSIZE_X*0.85, rely=2*PAD_UNIT, relwidth=COMP_FULLSIZE_X*0.15, relheight=COMP_FULLSIZE_Y*0.25)
        customtkinter.CTkLabel(self.master, text="Password", justify='right', anchor='e').place(relx=PAD_UNIT, rely=4*PAD_UNIT+COMP_FULLSIZE_Y*0.25, relwidth=COMP_FULLSIZE_X*0.15, relheight=COMP_FULLSIZE_Y*0.25)
        self.pwd_field = customtkinter.CTkEntry(self.master)
        self.pwd_field.insert(10, "PASSWORD")
        self.pwd_field.place(relx=2*PAD_UNIT+COMP_FULLSIZE_X*0.15, rely=4*PAD_UNIT+COMP_FULLSIZE_Y*0.25, relwidth=COMP_FULLSIZE_X*0.85+PAD_UNIT, relheight=COMP_FULLSIZE_Y*0.25)
        customtkinter.CTkLabel(self.master, text="OTP Code", justify='right', anchor='e').place(relx=PAD_UNIT, rely=6*PAD_UNIT+COMP_FULLSIZE_Y*0.5, relwidth=COMP_FULLSIZE_X*0.15, relheight=COMP_FULLSIZE_Y*0.25)
        self.otp_field = customtkinter.CTkEntry(self.master)
        self.otp_field.insert(10, "Codice")
        self.otp_field.place(relx=2*PAD_UNIT+COMP_FULLSIZE_X*0.15, rely=6*PAD_UNIT+COMP_FULLSIZE_Y*0.5, relwidth=COMP_FULLSIZE_X*0.85+PAD_UNIT, relheight=COMP_FULLSIZE_Y*0.25)

        customtkinter.CTkButton(self.master, text='DECRYPT', command=self.decrypt_callback).place(relx=.15, rely=8*PAD_UNIT+COMP_FULLSIZE_Y*3*0.25, relwidth=.3, relheight=COMP_FULLSIZE_Y*0.25)
        customtkinter.CTkButton(self.master, text='ENCRYPT', command=self.encrypt_callback).place(relx=.55, rely=8*PAD_UNIT+COMP_FULLSIZE_Y*3*0.25, relwidth=.3, relheight=COMP_FULLSIZE_Y*0.25)

        self.master.mainloop()

    def choose_dir(self):
        path = customtkinter.filedialog.askdirectory(initialdir='.', title='Select the folder to be encrypted/decrypted')

        self.path_comp.delete(0, customtkinter.END) #deletes the current value
        self.path_comp.insert(0, path)

        if path.endswith('\\') or path.endswith('/'):
            self.INPUT_PATH = path
        else:
            self.INPUT_PATH = path+'/'

        self.OUTPUT_PATH = path.rstrip('\\')
        self.OUTPUT_PATH = path.rstrip('/')
        self.LAST_FOLDER = os.path.os.path.basename(os.path.normpath(self.OUTPUT_PATH))
        self.DIR_LIST.append(self.INPUT_PATH)

    def encrypt_callback(self):
        self.KEY = hashlib.sha256(self.pwd_field.get().encode()).digest()

        print(self.otp_field.get())
        if self.totp.verify(self.otp_field.get()):
            self.master.quit()
            self.encrypt()
        else:
            self.OTP_counter+=1
            
        if self.OTP_counter==3:
            messagebox.showerror(title='ERROR', message='OTP Check failed')
            self.master.quit()

    def decrypt_callback(self):
        self.KEY = hashlib.sha256(self.pwd_field.get().encode()).digest()
        
        if self.totp.verify(self.otp_field.get()):
            self.master.quit()
            self.decrypt()
        else:
            self.OTP_counter+=1
            
        if self.OTP_counter==3:
            messagebox.showerror(title='ERROR', message='OTP Check failed')
            self.master.quit()

    def encrypt(self):
        '''
        Encrypt all the files found ricursively in PATH.
        '''

        #Find all the files contained recursively in the specified path
        self.find_files_recursive()
        #e.g. OUTPUT PATH = .../complete/path/encoded_dat/
        self.OUTPUT_PATH = self.INPUT_PATH[:-len(self.LAST_FOLDER)-1] + 'encoded_' + self.LAST_FOLDER + '/'
        #Copy the content of INPUT_PATH resursively in OUTPUT_PATH
        shutil.copytree(self.INPUT_PATH, self.OUTPUT_PATH)

        #Encrypt each file
        for x in self.FILE_LIST:
            print('Encoding '+colored(x, 'yellow')+' ...', end= '    ')

            #Read the binary content of a file
            with open(x, 'rb') as f:
                msg = f.read()    
            
            #Encrypt the content
            check, encrypted_msg = self.encrypt_msg(msg)

            if check:
                #Replace the content of the file with its encryption
                print(self.OUTPUT_PATH + x[len(self.INPUT_PATH):])
                
                with open(self.OUTPUT_PATH + x[len(self.INPUT_PATH):], 'wb') as f:
                    f.write(encrypted_msg)

                print(f'completed')
            else:
                print("it was already encrypted")                

    def decrypt(self):
        '''
        Decrypt all the files found ricursively in PATH.
        '''
        
        #Find all the files contained recursively in the specified path
        self.find_files_recursive()
        #e.g. OUTPUT PATH = .../complete/path/decoded_dat/
        self.OUTPUT_PATH = self.INPUT_PATH[:-len(self.LAST_FOLDER)-1] + 'decoded_' + self.LAST_FOLDER + '/'
        #Copy the content of INPUT_PATH resursively in OUTPUT_PATH
        shutil.copytree(self.INPUT_PATH, self.OUTPUT_PATH)

        #Decrypt each file
        for x in self.FILE_LIST:
            print('Decoding '+colored(x, 'yellow')+' ...', end= '    ')

            #Read the binary content of a file
            with open(x, 'rb') as f:
                msg = f.read()    
            
            #Decrypt the content
            check, decrypted_msg = self.decrypt_msg(msg)

            if check:
                print(self.OUTPUT_PATH)
                print(x[len(self.INPUT_PATH):])
                #Replace the content of the file with its decryption
                with open(self.OUTPUT_PATH + x[len(self.INPUT_PATH):], 'wb') as f:
                    f.write(decrypted_msg)

                print('completed')
            else:
                print("it wasn't already encrypted")


    def encrypt_msg(self, msg):
        '''
        Encrypt a bytes message with AES.

        Args:
            msg (bytes): Message to be encrypted

        Returns:
            check (bool): True if the file msg wasn't already encrypted
                          False otherwise

            encoded_msg (bytes): Encrypted message
        '''

        if self.CHECK_ENCRYPTED == msg[:len(self.CHECK_ENCRYPTED)]:
            #The message was already encrypted
            return False, None
        else:
            #Padding msg
            msg = self.pad_msg(msg)
            #Initialization vector
            IV = Random.new().read(AES.block_size)
            #AES cipher with Cipher Block Chaining (CBC) techinque
            cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
            #Message encrypted
            return True, self.CHECK_ENCRYPTED + IV + cipher.encrypt(msg)

    def decrypt_msg(self, msg):
        '''
        Decrypt a bytes message with AES.

        Args:
            msg (bytes): Message to be decrypted

        Returns:
            check (bool): True if the file msg was already encrypted
                          False otherwise
                          
            encoded_msg (bytes): Decrypted message
        '''
        
        if self.CHECK_ENCRYPTED == msg[:len(self.CHECK_ENCRYPTED)]:
            msg = msg[len(self.CHECK_ENCRYPTED):]
            #Initialization vector (beginning of the encoded text)
            IV = msg[:AES.block_size]
            #AES cipher with Cipher Block Chaining (CBC) techinque
            cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
            #Message decrypted (from IV on)
            decoded_msg = cipher.decrypt(msg[AES.block_size:])
            #Message decrypted without last padding bytes
            return True, decoded_msg.rstrip(b"\0")
        else:
            #The message wasn't already encrypted
            return False, None


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


def main():
    #Initialization of Authenticator MFA
    #with open('key.txt') as f:
        #otp_key=base64.b32encode(f.readline().encode())
    #uri = pyotp.totp.TOTP(OTP_KEY).provisioning_uri(name='ExampleName',
    #                                                issuer_name='Encrypter/Decrypter App')
    #print(uri)
    #qrcode.make(uri).save("OTP.png")

    #Use already initialized Authenticator
    otp_key = ''
    with open('key.txt') as f:
        otp_key=base64.b32encode(f.readline().encode())

    cypher = CipherData(otp_key)

if __name__=='__main__':
    main()
