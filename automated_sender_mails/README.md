# Automated mail sender
The following programs could be useful during a Phishing campaign to trust the sender e-mail address.
The sender keeps sending mails, one at every 30 minutes, to some e-mail addresses.
This approach is useful to trust sender domain and mail address, trying to elude basic anti-spam tools (e.g. Google ones) that could block the mails from:
- domains created from less than 28 days;
- e-mail addresses that aren't active (they could be suspicious).

## Requirements
To install required python modules, you need to type the following command:


## Gmail automated sender
1. You need to specify sender password as one of the command line arguments.
```bash
pip3 install -r requirements.txt
```

## AWS SES automated sender
1. Create the AWS key.
2. Then create a new file on your sistem, with the following path:

| System      | Path                                 |
| ----------- | ------------------------------------ |
| Linux       | `~/.aws/credentials`                 |
| Windows     | `C:/Users/USERNAME/.aws/credentials` |

3. Type the following lines in the file:
```bash
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```
4. Update **AWS_REGION** in the code with region of your AWS machines.
