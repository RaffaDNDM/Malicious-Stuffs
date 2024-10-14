# Backdoor
On the victim side, running [backdoor.py](backdoor.py), a reverse shell is opened and the attacker can detect that the victim runs it by receiving a request from [backdoor.py](backdoor.py) during the execution of [backdoor_server.py](backdoor_server.py). So the attacker can execute terminal commands by writing them on [backdoor_server.py](backdoor_server.py) and then they will be executed on the victim machine.<br>
To use this program, you need to install the following python modules, through this command:
```bash
pip3 install argparse termcolor
```
or<br>
```bash
pip3 install -r requirements.txt
```