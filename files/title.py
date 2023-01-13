from sys import platform
import os
import os.path


def p_title():
    print("""
 ____                                  _  __  __                                         
|  _ \   __ _  ___  ___ __      __  __| ||  \/  |  __ _  _ __    __ _   __ _   ___  _ __ 
| |_) | / _` |/ __|/ __|\ \ /\ / / / _` || |\/| | / _` || '_ \  / _` | / _` | / _ \| '__|
|  __/ | (_| |\__ \\__ \ \ V  V / | (_| || |  | || (_| || | | || (_| || (_| ||  __/| |   
|_|     \__,_||___/|___/  \_/\_/   \__,_||_|  |_| \__,_||_| |_| \__,_| \__, | \___||_|   
                                                                       |___/             

                                                                |----------------|
                                                                | By Roger Fibla |
                                                                |----------------|
        
        
    Press intro to continue
""")

    input("")
    
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "win64":
        os.system('cls')
