#!/usr/bin/python3

#
# Password Manager
# By Aria
#

import string
import random
from time import sleep

import os
import os.path
from getpass import getpass
import hashlib
from sys import platform
import json
import base64

from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Function to clear the terminal
def clear():
    if platform == "linux" or platform == "linux2":
        os.system('clear')
    elif platform == "win64" or platform == "win32":
        os.system('cls')


# Main title of the program
def title():
    print("""
 ____                                  _  __  __                                         
|  _ \\   __ _  ___  ___ __      __  __| ||  \\/  |  __ _  _ __    __ _   __ _   ___  _ __ 
| |_) | / _` |/ __|/ __|\\ \\ /\\ / / / _` || |\\/| | / _` || '_ \\  / _` | / _` | / _ \\| '__|
|  __/ | (_| |\\__ \\__ \\ \\ V  V / | (_| || |  | || (_| || | | || (_| || (_| ||  __/| |   
|_|     \\__,_||___/|___/  \\_/\\_/   \\__,_||_|  |_| \\__,_||_| |_| \\__,_| \\__, | \\___||_|   
                                                                       |___/             

    Press intro to continue
          """)


# the key() functions creates a key based on your password. This key is used to encrypt passwords later
def key(PA):
    with open(PA + "data/temp_file.txt", "r") as tf:
        raw_passwd = tf.read()

    password = raw_passwd.encode()

    mysalt = b'\xbb\x9c\xdfu\xee\x99\xe3e\xce\x9e\xff*\xb3):r'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )

    encoded_key = base64.urlsafe_b64encode(kdf.derive(password))

    key = encoded_key.decode()
    return key

def mainWin():
    return 0

def mainLinux():
    # Check if there is an account: if not a password is created and encrypted
    PATH_L = os.path.expanduser("~/.config/PasswdManager/")

    if not os.path.exists(PATH_L):
        # path structure ~/.config/PasswdManager/
        # .
        # ├── data.json
        # └── passwd
        #     └── info.txt
        #     └── passwd1.txt
        #     └── passwd2.txt

        os.makedirs(PATH_L)
        os.makedirs(PATH_L + "data")
        os.makedirs(PATH_L + "data/passwd")

        with open(PATH_L + "data/data.json", "w+") as json_f:
            json_f.write('{"created_passwords": []}')
        with open(PATH_L + "data/passwd/info.txt", "w+") as txt_f:
            txt_f.write("The passwords will be stored encoded in this directory")

        print("Create a password. This password will be encrypted.")
        login_passwd = getpass(">> ")

        encrypted_passwd = hashlib.md5(login_passwd.encode()).hexdigest()
        
        os.makedirs(PATH_L + "data/passwd", exist_ok=True)
        with open(PATH_L + "data/passwd/passwd.txt", "w+") as f:
            f.write(encrypted_passwd)

        del login_passwd
    else:
        pass

    clear()

    title()

    # login
    with open(PATH_L + "data/passwd/passwd.txt", "r") as f:
        file = f.read()

    while True:
        print("Enter your password.")
        login = getpass(">> ")
        login_e = hashlib.md5(login.encode()).hexdigest()

        if login_e in file:
            print("Correct password!")
            break
        else:
            print("Incorrect password, try again.")

    with open(PATH_L + "data/temp_file.txt", "w+") as tf:
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
        '5' → How secure is my password?
        'q' → Exit the program
              """)

        choice = input(">> ")

        if choice == "info":
            print("Welcome to PasswdManager, a simple password manager made with python. With this program, you can easily store all your passwords encrypted in a very secure way. Enjoy\n\nTo delete everything just type 'deleteall' in the main page")

            input("\nPress enter to continue ")
            clear()

        elif choice == "passwd":
            with open(PATH_L + 'data/data.json') as jf:
                data = json.load(jf)

            num = 0
            for pass_name in data["created_passwords"]:
                num += 1
                print(f"{num}. '{pass_name}'\n")

            input("\nPress enter to continue ")
            clear()

        elif choice == "1":
            cipher = Fernet(key(PATH_L))

            print("Enter the name of the password.")
            input_name = input(">> ")
            filename = PATH_L + "data/passwd/" + input_name + ".txt"

            print("Create a password. This password will be encrypted.")
            create_passwd_ = getpass(">> ")

            with open(filename, "wb") as f:
                f.write(create_passwd_.encode())

            with open(filename, "rb") as ef:
                e_file = ef.read()

            encrypted_passwd = cipher.encrypt(e_file)

            with open(filename, "wb") as ef:
                ef.truncate(0)
                ef.write(encrypted_passwd)

            with open(PATH_L + "data/data.json", 'r+') as jf:
                file_data = json.load(jf)
                file_data["created_passwords"].append(input_name)
                jf.seek(0)
                json.dump(file_data, jf, indent=4)

            del create_passwd_

            input("\nPress enter to continue ")
            clear()

        elif choice == "2":
            cipher = Fernet(key(PATH_L))

            print("Enter the name of the password")
            file_name = input(">> ")
            file_path = PATH_L + "data/passwd/" + file_name + ".txt"

            with open(file_path, "rb") as df:
                encrypted_data = df.read()

            passwd = cipher.decrypt(encrypted_data)

            print("\n" + passwd.decode())

            input("\nPress enter to continue ")
            clear()

        elif choice == "3":
            print("Enter the name of the password you want to delete.")
            passwd_name = input(">> ")

            print("Are you sure you want to delete the password? [y/N]")
            confirmation = input(">> ")

            path = (PATH_L + "data/passwd/" + passwd_name + ".txt")

            if confirmation == "y" or confirmation == "Y" or confirmation == "yes" or confirmation == "YES":
                if os.path.exists(path):
                    os.remove(path)

                    with open(PATH_L + 'data/data.json') as js:
                        data = json.load(js)

                    n = 0
                    for passwd in data["created_passwords"]:
                        if passwd == passwd_name:
                            data["created_passwords"].pop(n)
                            break
                        else:
                            n += 1

                    with open(PATH_L + 'data/data.json', 'w') as file:
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

        elif choice == "5":
            clear()
            print("Enter your password to see how secure it is:")

            password = str(getpass(">> "))

            if password == "":
                print("password must be at least 1 char long")

            else:
                length_criteria = 8
                uppercase_criteria = 1
                lowercase_criteria = 1
                digit_criteria = 1
                special_char_criteria = 1

                score = 0
                max_score = (
                    length_criteria
                    + uppercase_criteria
                    + lowercase_criteria
                    + digit_criteria
                    + special_char_criteria
                )
                if len(password) >= length_criteria:
                    score += length_criteria
                if any(char.isupper() for char in password):
                    score += uppercase_criteria
                if any(char.islower() for char in password):
                    score += lowercase_criteria
                if any(char.isdigit() for char in password):
                    score += digit_criteria
                if any(not char.isalnum() for char in password):
                    score += special_char_criteria

                strength_percentage = int((score / max_score) * 100)

                print(f"\nYour password is {strength_percentage}% secure")

                if strength_percentage < 25:
                    print("You must use a better password! >:(")
                elif 25 <= strength_percentage < 50:
                    print("You should use a better password :c")
                elif strength_percentage == 50:
                    print("Your password is a bit meh, improve it :v")
                elif 50 < strength_percentage <= 75:
                    print("Your password is okay, but it could be better! :>")
                else:
                    print("You have a nice and strong password! :3")

            input("Press enter to continue ")
            clear()

        elif choice == "deleteall":
            print("are you sure you want to delete all your passwords and information? [y/N]")

            finRes = input(">> ")
            
            if finRes == "y" or finRes == "Y" or finRes == "yes":
                os.system(f"rm -rf {PATH_L}")
                print("Bye")
                sleep(1)
                quit()

            else:
                print("The information will not be deleted")
                input("\nPress enter to continue")
                clear()

        elif choice == "q":
            print("Exiting...\nBye")
            sleep(1)
            break

        else:
            print("Command not recognized. Please try again.")
            input("\nPress enter to continue")
            clear()


def main():
    if platform == "linux" or platform == "linux2":
        mainLinux()
        mainWin()
    else:
        print("Not aviable yet.")
        quit()



if __name__ == "__main__":
    try:
        main()
    except:
        print("Program crashed. Deleting temp files")
        
    if platform == "linux" or platform == "linux2":
        
        PATH_L = os.path.expanduser("~/.config/PasswdManager/")

        with open(PATH_L + "data/temp_file.txt","r+") as tf_f:
            tf_f.truncate(0)
            tf_f.close()
        os.remove(PATH_L + "data/temp_file.txt")
    
# :3
