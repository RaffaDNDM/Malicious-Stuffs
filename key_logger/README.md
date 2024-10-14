# Key logger
To use the following Key Logger program, you need to install the module pynput by typing on command line:
```bash
pip3 install pynput smtplib
```
or<br>
```bash
pip3 install -r requirements.txt
```
To run the program, you need to type for example this command on bash:
```bash
python3 run_logger.py -t 6
```
where <i>6</i> is the refresh time. Hence every <i>6 seconds</i>, the program will send the obtained log info to specified mail address. <br>
To check which parameters you can insert, you can type the command:
<pre lang="bash"><code>python3 run_logger.py --help </code></pre>
The program must run with superuser privileges.


### Credentials file
To run correctly the program, you need to add a file, called <code>credentials.txt</code> in the same directory of the program. The file must contains a line with this info in this format:
<pre lang="bash"><code>example@gmail.com password</code></pre>
where <b>example@gmail.com</b> must be replaced by the google mail (<i>smtp.gmail.com</i> that works on port <i>587</i>) that you want to use and <b>password</b> is the relative password.<br>
Sometimes Windows put the program in quarantine. Remember that you need to abilitate less secure apps reception, because by default Google prevents the reception of e-mail by not trusted apps.
