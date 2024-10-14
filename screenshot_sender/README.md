# Send victim's screenshot
The program takes a shot of the screen and sends it to the specified mail address.<br> 
To use this program, you need to install the following python modules, through this command:
```bash
pip3 install argparse termcolor smtplib
```
or<br>
```bash
pip3 install -r requirements.txt
```
<pre lang="bash"><code>python3 -m pip install pyautogui</code></pre>
<pre lang="bash"><code>pip3 install argparse</code></pre>
To run the program, you need to type the following command on terminal:
<pre lang="bash"><code>python3 screenshot_sender.py</code></pre>

### Credentials file
To run correctly the program, you need to add a file, called <code>credentials.txt</code> in the same directory of the program. The file must contains a line with this info in this format:
<pre lang="bash"><code>example@gmail.com password</code></pre>
where <b>example@gmail.com</b> must be replaced by the google mail (<i>smtp.gmail.com</i> that works on port <i>587</i>) that you want to use and <b>password</b> is the relative password.<br>
Sometimes Windows put the program in quarantine. Remember that you need to abilitate less secure apps reception, because by default Google prevents the reception of e-mail by not trusted apps.
