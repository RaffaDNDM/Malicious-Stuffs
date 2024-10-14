# Self replicant virus
In this folder, the replication process of a virus was analysed by developing a virus. The subfolders are:
<details><summary><i><b>src_client</b></i></summary>
It contains the file [self_replicant_virus.py](src_client/self_replicant_virus.py) that if it is executed on the victim machine, it will replicate the malicious code in all the python scripts contained in the folder. Every time a program with this malicious code is executed, it will work as usual but it also execute in backgroung the malicious code, replicating it in other python programs and sending information to the remote server.
```bash
pip3 install glob2
```
</details>
<details><summary><i><b>src_server</b></i></summary>
It contains the file [server.py](src_server/server.py) that gathers information from the execution of the virus on the client side. For example, in this case it receives the list of the content of the directory in which an infected file is and it's executed by the victim.
To run the program in the folder, you need to install some dependencies with this terminal command:
```bash
pip3 install termcolor
```
</details>
