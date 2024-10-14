#######################
# @author: RaffaDNDM
# @date:   2022-03-12
#######################

import schedule
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import argparse
from termcolor import cprint

# Create our email message 'msg'
def message(subject="Subject", text="", img=None, attachment=None):
    
    # build message contents
    msg = MIMEMultipart()
      
    # Add Subject
    msg['Subject'] = subject  
      
    # Add text contents
    msg.attach(MIMEText(text))  
  
    # Check if we have anything given in the img parameter
    if img is not None:
        # Check whether we have the lists of images or not!
        if type(img) is not list:
            # if it isn't a list, make it one
            img = [img]  
  
        # Now iterate through our list
        for one_img in img:
            
            # Read the image binary data
            img_data = open(one_img, 'rb').read()  
              
            # Attach the image data to MIMEMultipart using MIMEImage, we add the given filename use os.basename
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))
  
    # We do the same for attachments as we did for images
    if attachment is not None:
  
        # Check whether we have the lists of attachments or not!
        if type(attachment) is not list:
            # if it isn't a list, make it one
            attachment = [attachment]  
  
        for one_attachment in attachment:
  
            with open(one_attachment, 'rb') as f:
                
                # Read in the attachment using MIMEApplication
                file = MIMEApplication(
                    f.read(),
                    name=os.path.basename(one_attachment)
                )
            file['Content-Disposition'] = f'attachment;\
            filename="{os.path.basename(one_attachment)}"'
              
            # At last, Add the attachment to our message object
            msg.attach(file)

    return msg
  
# send our email message 'msg' to targets
def mail_send(smtp, sender, receiver, msg):
    # Provide some data to the sendmail function!
    smtp.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string()) 
  
def arg_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-mail", "-m", "-s", "-sender", dest="sender", help="e-mail address of the sender")
    parser.add_argument("-password", "-pwd", "-p", dest="pwd", help="Password of the sender")
    parser.add_argument("-to", "-target", dest="targets", help="")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.targets:
        parser.print_help()
        exit(1)
        
    if not args.sender:
        parser.print_help()
        exit(1)

    if not args.pwd:
        parser.print_help()
        exit(1)
    
    sender=args.sender
    print("\n")
    cprint('Sender:   ', 'yellow', attrs=['bold',], end='')
    print(f'{sender}')

    pwd=args.pwd
    cprint('Password:  ', 'green', attrs=['bold',], end='')
    print(f'{pwd[0]}{"*"*(len(pwd)-2)}{pwd[-1]}')

    targets=(args.targets.replace(" ","")).split(",")
    cprint('Targets:   ', 'blue', attrs=['bold',], end='')
    print(targets, end='\n\n')

    return sender, pwd, targets


def main():
    sender, pwd, targets= arg_parser()
    # initialize connection to our email server, we will use gmail here
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    smtp.starttls()
        
    # Login with your email and password
    smtp.login(sender, pwd)

    # Call the message function
    msg = message(subject="Weather", 
                  text="Goodmorning,\n"+
                       "we contact you from Weather.IO newsletter. It will rain all the weekend.\n\n"+
                       "Have a nice day,\n"+"Weather.IO",
                  img='resources/weather.jpg') 
    
    mail_send(smtp, sender, targets, msg)
    schedule.every(10).minutes.do(mail_send, smtp=smtp, sender=sender, receiver=targets, msg=msg)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        # Finally, don't forget to close the connection
        smtp.quit()

if __name__=="__main__":
    main()