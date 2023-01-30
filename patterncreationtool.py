print("Importing needs...")

import os
from time import sleep
def clr():
    #Checks if windows. If so sets clrcmd to "clr". If linux runs "clear".
    if os.name=="nt": clrcmd = "cls"
    if os.name=="posix": clrcmd = "clear"
    # Runs the command in the var clrcmd
    os.system(clrcmd)
# Sets working directory to patterns
os.chdir(os.getcwd() + "/patterns")



# MAIN
clr()
filename = input("\n\nWhat do you want the file to be called?\n")
filename = filename + '.py'
print("Creating base.")
fs = open(file=filename, mode='w')
fs.write("")
fs.close()
fs = open(file=filename, mode='a')
fs.write(
    """
from util import key_press, import_pdx

from time import sleep


pdx = import_pdx()
    
# GENERATED WITH FINS PATTERN CREATION TOOL VERY COOL
    
def execute():
    pdx.mouseDown()
    """
)
print("Now ready.")
## Ask for how many blocks to go forward or direction
clr()
while True:
    clr()
    #Get command
    cmd = input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPlease type a command.\n\nType /help to get commands.\n\n")
    if cmd == "/help":
        clr()
        print("\n\nWait 1: sleep\nGo Foward 1: fw\nGo right 1: r\nGo Left 1: l\n\nGo Forward/Left/Right 2+: fw2/r2/l2\n\nDone with creating pattern?: comp\n")
        sleep(5)
    if cmd.startswith("sleep"):
        amt = input("How long do you want to wait?")
        fs.write("os.wait(" + amt + ")\n")
    if cmd.startswith("fw"):
        if cmd[2]:
            amt = cmd[2]
        else:
            amt = "1"
        fs.write("key_press(\"w\", " + amt + ")\n")
    if cmd.startswith("r"):
        if cmd[1]:
            amt = cmd[1]
        else:
            amt = "1"
        fs.write("key_press(\"d\", " + amt + ")\n")
    if cmd.startswith("l"):
        if cmd[1]:
            amt = cmd[1]
        else:
            amt = "1"
        fs.write("key_press(\"a\", " + amt + ")\n")
    if cmd.startswith("comp"):
        print("Alright!")
        break


print("File complete!")