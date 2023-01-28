#PasswdManager
#By Roger Fibla
#2022

import os
from getpass import getpass
import hashlib
import os.path

from files.clear import clear


#Create acount

if os.path.exists(".data/passwd/passwd.txt") == True:
    pass

else:
    f = open(".data/passwd/passwd.txt", "a")
    create_passwd = getpass("Create a password. This password will be encrypted.\n>> ")

    encrypted_passwd = hashlib.md5(create_passwd.encode())

    f.write(encrypted_passwd.hexdigest())
    f.close()

    del(create_passwd)

    clear()

from files.login import login
from files.title import p_title


#Main title

p_title()

login()

from files.passwd_gen import passwd_gen
from files.import_passwd import import_passwd
from files.see_password import show_passwd
from files.all_passwd import display_passwd
from files.delete_passwd import delete_passwd
from files.intro import introduction


#Main Choice - Loop

i = 1

while i != 0:

    print("Select one of the different options! Type 'info' to a full explanation of the program\n")
    
    print("See password names: 'passwd'\n\nImport a new password: '1'\nSee a password: '2'\nDelete a password: '3'\nGenerate a password: '4'\n\nQuit the program: 'q'")

    choice = input(">> ")

    clear()

    if choice == "info":
        introduction()
        input("\nPress enter to continue ")

    elif choice == "passwd":
        display_passwd()
        input("\nPress enter to continue ")

    elif choice == "1":
        import_passwd()

    elif choice == "2":
        show_passwd()
        input("\nPress enter to continue ")

    elif choice == "3":
        delete_passwd()

    elif choice == "4":
        passwd_gen()
        input("\nPress enter to continue ")


    elif choice == "q":
        i = 0
    
    else:
        print("Command not recognized. Please try again.")
        input("Press enter to continue ")

    clear()


# delete temp files

with open(".data/temp_file.txt","r+") as tf_f:
    tf_f.truncate(0)
    tf_f.close()
    
os.remove(".data/temp_file.txt")
