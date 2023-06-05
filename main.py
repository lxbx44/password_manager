#!/usr/bin/env python

#
# Password Manager
# By Aria
#

import string
import random
from time import sleep

import os, os.path
from getpass import getpass
import hashlib
from sys import platform
import json
import base64

from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def clear():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "win64":
        os.system('cls')
    elif platform == "win32":
        os.system('cls')

def title():
    print("""
 ____                                  _  __  __                                         
|  _ \\   __ _  ___  ___ __      __  __| ||  \\/  |  __ _  _ __    __ _   __ _   ___  _ __ 
| |_) | / _` |/ __|/ __|\\ \\ /\\ / / / _` || |\\/| | / _` || '_ \\  / _` | / _` | / _ \\| '__|
|  __/ | (_| |\\__ \\__ \\ \\ V  V / | (_| || |  | || (_| || | | || (_| || (_| ||  __/| |   
|_|     \\__,_||___/|___/  \\_/\\_/   \\__,_||_|  |_| \\__,_||_| |_| \\__,_| \\__, | \\___||_|   
                                                                       |___/             

                                                                |---------|
                                                                | By Aria |
                                                                |---------|                
    Press intro to continue
          """)


def key():
    with open(".data/temp_file.txt", "r") as tf:
        raw_passwd = tf.read()

    password = raw_passwd.encode()

    mysalt = b'\xbb\x9c\xdfu\xee\x99\xe3e\xce\x9e\xff*\xb3):r'

    kdf = PBKDF2HMAC (
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )

    encoded_key = base64.urlsafe_b64encode(kdf.derive(password))

    key = encoded_key.decode()
    return key


def main():

    # Check if there is an account: if not a password is created and encrypted
    if os.path.exists(".data/passwd/passwd.txt") == True:
        pass
    else:
        print("Create a password. This password will be encrypted.")
        login_passwd = getpass(">> ")

        encrypted_passwd = hashlib.md5(login_passwd.encode())

        with open(".data/passwd/passwd.txt", "a") as f:
            f.write(encrypted_passwd.hexdigest())
            f.close()

        del(login_passwd)

    clear()

    title()

    # login

    with open(".data/passwd/passwd.txt", "r") as f:
        file = f.read()
    
    
    while True:
        print("Enter your password.")
        login = getpass(">> ")
        login_e = hashlib.md5(login.encode())
        login_f = login_e.hexdigest()
        
        if login_f in file:
            print("Correct password!")
            break
        else:
            print("Incorrect password, try again.")

    
    with open(".data/temp_file.txt", "a") as tf:
        tf.write(login)

    clear()
    # Main loop

    while True:    
        print("""
    Select one of the different options! Type 'info' to a full explanation of the program
    
        'passwd' → See current password names
        '1' → Import a new password
        '2' → Search for a password
        '3' → Delete a password
        '4' → Generate a new secure password
        'q' → Exit the program
              """)
    

        choice = input(">> ")

        if choice == "info":
            print("Welcome to PasswdManager, a simple password manager, coded in Python by Aria. With this program, you can store all your passwords encrypted in a secure way.")
            input("\nPress enter to continue ")
            clear()


        elif choice == "passwd":
            with open('.data/data.json') as jf:
                data = json.load(jf)

            num = 0
            for pass_name in data["created_passwords"]:
                num += 1
                print(f"{num}. '{pass_name}'\n")
            
            input("\nPress enter to continue ")
            clear()


        elif choice == "1":
            cipher = Fernet(key())
            
            print("Enter the name of the password.")
            input_name = input(">> ")
            filename = ".data/passwd/" + input_name + ".txt"

            print("Create a password. This password will be encrypted.")
            create_passwd_ = getpass(">> ")
        
            with open(filename, "w") as f:
                f.write(create_passwd_)
                f.close()

            with open(filename, "rb") as ef:
                e_file = ef.read()

            ectypted_passwd = cipher.encrypt(e_file)

            with open(filename, "ab") as ef:
                ef.truncate(0)
                ef.write(ectypted_passwd)

            with open(".data/data.json",'r+') as jf:
                file_data = json.load(jf)
                file_data["created_passwords"].append(input_name)
                jf.seek(0)
                json.dump(file_data, jf, indent = 4)
        
        
            del(create_passwd_)

            input("\nPress enter to continue ")
            clear()


        elif choice == "2":
            cipher = Fernet(key())
            
            print("Enter the name of the password")
            file_name = input(">> ")
            file_path = ".data/passwd/" + file_name + ".txt"
            
            with open(file_path, "rb") as df:
                encrypted_data = df.read()
            
            passwd = cipher.decrypt(encrypted_data)

            print("\n" + passwd.decode())

            input("\nPress enter to continue ")
            clear()


        elif choice == "3":
            print("Enter the name of the passwdord you want to delete.")
            passwd_name = input(">> ")

            print("Are you sure you want to delete the passwdord? [y/N]")
            confirmation = input(">> ")
            
            path = (".data/passwd/" + passwd_name + ".txt")

            if confirmation == "y" or confirmation == "Y" or confirmation == "yes" or confirmation == "YES":
                if os.path.exists(path):
                    os.remove(path)

                    with open('.data/data.json') as js:
                        data = json.load(js)
                    
                    n = 0
                    for passwd in data["created_passwords"]:
                        if passwd == passwd_name:
                            data["created_passwords"].pop(n)
                            break
                        else:
                            n += 1
                            
                    with open('.data/data.json', 'w') as file: 
                        json.dump(data, file) 
                          



                else:
                    print("\nPassword not recognized.\nPlease try again.")
            else:
                pass

            
            input("\nPress enter to continue ")
            clear()


        elif choice == "4":
            characters = list(string.ascii_letters + string.digits + "!@#$%^&*")

            print("Enter the length of the password.")
            length = int(input(">> "))

            random.shuffle(characters)

            password = []

            for i in range(length):
                char = random.choice(characters)
                password.append(char)

            random.shuffle(password)

            print("Your password is " + "".join(password))


            input("\nPress enter to continue ")
            clear()

        elif choice == "q":
            print("Bye")
            sleep(1)
            break
            

        else:
            print("Command not recognized. Please try again.")
            input("\nPress enter to continue")
            clear()




if __name__ == "__main__":
    try:
        main()
    except:
        print("Program crashed. Deleting temp files")
        pass

    with open(".data/temp_file.txt","r+") as tf_f:
        tf_f.truncate(0)
        tf_f.close()
    os.remove(".data/temp_file.txt")
    
# :3