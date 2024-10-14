#######################
# @author: RaffaDNDM
# @date:   2022-03-15
#######################

import schedule
import boto3
import argparse
from termcolor import cprint
from botocore.exceptions import ClientError
  
def mail_send(SES_client, sender, receiver):
    CHARSET = "UTF-8"
    SUBJECT="Weather" 

    BODY_TEXT="Goodmorning,\r\nwe contact you from Weather.IO newsletter. It will rain all the weekend.\r\n\r\nHave a nice day,\r\nnWeather.IO"
    BODY_HTML="""<html>
                    <head></head>
                    <body>
                        <p>Goodmorning,<br>
                        we contact you from Weather.IO newsletter. It will rain all the weekend.<br><br>
                        Have a nice day,<br>
                        Weather.IO</p>
                    </body>
                </html>
            """

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = SES_client.send_email(
            Destination={
                'ToAddresses': receiver,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=sender,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def arg_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-from", "-s", "-sender", dest="sender", help="e-mail address of the sender")
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

    sender=args.sender
    print("\n")
    cprint('Sender:   ', 'yellow', attrs=['bold',], end='')
    print(f'{sender}')

    targets=(args.targets.replace(" ","")).split(",")
    cprint('Targets:   ', 'blue', attrs=['bold',], end='')
    print(targets, end='\n\n')

    return sender, targets


def main():
    sender, targets= arg_parser()
    
    #Amazon SES registered region
    AWS_REGION = "us-east-1"

    #Initialize connection to Amazon SES
    SES_client = boto3.client('ses',region_name=AWS_REGION)
    
    mail_send(SES_client, sender, targets)
    schedule.every(30).minutes.do(mail_send, SES_client=SES_client, sender=sender, receiver=targets)

    try:
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        # End of mail sending process
        exit(0)

if __name__=="__main__":
    main()