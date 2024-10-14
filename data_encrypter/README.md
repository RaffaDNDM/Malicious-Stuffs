# Data encrypter
The program recursively performs the encryption of the files in a folder by specifying a password. To run the program, you need to install the following modules for python3, through this command:
```bash
pip3 install pycrypto termcolor argparse glob2 tkinter hashlib pyotp
```
or<br>
```bash
pip3 install -r requirements.txt
```
To run the program, you need to type for example this command on bash:
```bash
python3 arp_network_scanner.py -net 192.168.1.0/24 
```
An example of output of the command is shown in the following image:<br>
<img src="output.png" width="600" alt="output"><br>
To check which parameters you can insert, you can type the command:
```bash
python3 arp_network_scanner.py --help 
```
The program must run with superuser privileges.
