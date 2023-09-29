#!/usr/bin/python3

#
# Password Manager
# By Ari:3
#

import string
import random
from time import sleep
from terminaltables import SingleTable

import os
import os.path
from shutil import rmtree
from getpass import getpass
import hashlib
import sys
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
    else:
        print("Not aviable yet")
        sys.exit(1)


# the key() functions creates a key based on your password. This key is used to encrypt passwords later
def key(PA):
    raw_passwd = PA

    password = raw_passwd.encode()

    mysalt = b'\xbb\x9c\xdfu\xee\x99\xe3e\xce\x9e\xff*\xb3):r'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )

    try:
        encoded_key = base64.urlsafe_b64encode(kdf.derive(password))
    except Exception as e:
        print(f"Error encoding password's key\n{e}")

    key = encoded_key.decode()
    return key


def mainWin():
    return "Not aviable yet"


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

        try:
            os.makedirs(PATH_L)
            os.makedirs(PATH_L + "data")
            os.makedirs(PATH_L + "data/passwd")
        except Exception as e:
            print(f"Error creating folders\n{e}")

            if os.path.exists(PATH_L):
                rmtree(PATH_L)
            sys.exit(1)

        with open(PATH_L + "data/data.json", "w+") as json_f:
            json_f.write('{"created_passwords": []}')
        with open(PATH_L + "data/passwd/info.txt", "w+") as txt_f:
            txt_f.write("The passwords will be stored encoded in this directory")

        print("Create a password. This password will be encrypted.")
        login_passwd = getpass(">> ")

        try:
            encrypted_passwd = hashlib.md5(login_passwd.encode()).hexdigest()
        except Exception as e:
            print(f"Error encoding password\n{e}")
            rmtree(PATH_L)
            sys.exit(1)

        os.makedirs(PATH_L + "data/passwd", exist_ok=True)

        try:
            with open(PATH_L + "data/passwd/passwd.txt", "w+") as f:
                f.write(encrypted_passwd)
        except Exception as e:
            print(f"Error encrrypting password\n{e}")
            rmtree(PATH_L)
            sys.exit(1)

        del login_passwd

    clear()

    # MAIN TITLE
    print("Password Manager :3")

    # login
    try:
        with open(PATH_L + "data/passwd/passwd.txt", "r") as f:
            file = f.read()
    except Exception as e:
        print(f"Error opening password file\n{e}")
        sys.exit(1)

    while True:
        print("Enter your password.")
        login = getpass(">> ")
        login_e = hashlib.md5(login.encode()).hexdigest()

        if login_e in file:
            print("Correct password!")
            break
        else:
            print("Incorrect password, try again.")

    clear()
    # Main loop
    while True:
        print("Select one of the different options! Type 'info' to a full explanation of the program\n")

        TABLE_DATA = (
            ('command', 'functionality'),
            ("'passwd'", "See current password names"),
            ("'1'", "Import a new password"),
            ("'2'", "Search for a password"),
            ("'3'", "Delete a password"),
            ("'4'", "Generate a new secure password"),
            ("'5'", "How secure is my password?"),
            ("'q'", "Exit the program")
        )

        table_cont = SingleTable(TABLE_DATA)
        table_cont.justify_columns[1] = 'left'
        print(table_cont.table)

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
            try:
                cipher = Fernet(key(login))
            except Exception as e:
                print(f"Error getting key\n{e}")
                sys.exit(1)

            print("Enter the name of the password.")
            input_name = input(">> ")
            filename = PATH_L + "data/passwd/" + input_name + ".txt"

            print("Create a password. This password will be encrypted.")
            create_passwd_ = getpass(">> ")

            with open(filename, "wb") as f:
                try:
                    f.write(create_passwd_.encode())
                except Exception as e:
                    print(f"Error writing password\n{e}")
                    os.rename(filename)
                    sys.exit(1)

            with open(filename, "rb") as ef:
                e_file = ef.read()

            try:
                encrypted_passwd = cipher.encrypt(e_file)
            except Exception as e:
                print(f"Error encrypting password\n{e}")
                os.remove(filename)

            with open(filename, "wb") as ef:
                ef.truncate(0)
                ef.write(encrypted_passwd)

            with open(PATH_L + "data/data.json", 'r+') as jf:
                try:
                    file_data = json.load(jf)
                    file_data["created_passwords"].append(input_name)
                    jf.seek(0)
                    json.dump(file_data, jf, indent=4)
                except Exception as e:
                    print(f"Error adding password to json\n{e}")
                    os.remove(filename)

            del create_passwd_

            input("\nPress enter to continue ")
            clear()

        elif choice == "2":
            try:
                cipher = Fernet(key(login))
            except Exception as e:
                print(f"Error getting key\n{e}")
                sys.exit(1)

            print("Enter the name of the password")
            file_name = input(">> ")
            file_path = PATH_L + "data/passwd/" + file_name + ".txt"

            if os.path.exists(file_path):
                with open(file_path, "rb") as df:
                    encrypted_data = df.read()

                passwd = cipher.decrypt(encrypted_data)

                print("\n" + passwd.decode())

                input("\nPress enter to continue ")
                clear()
            else:
                print("Password doesn't exist")

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
                    print("\nPassword not recognized.\nPlease make sure the password exists and try again.")
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

            elif " " in password:
                print("Password should have spaces")

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
                sleep(0.5)
                sys.exit(1)

            else:
                print("The information will not be deleted")
                input("\nPress enter to continue")
                clear()

        elif choice == "q":
            print("Exiting...\nBye")
            sleep(0.5)
            break

        else:
            print("Command not recognized. Please try again.")
            input("\nPress enter to continue")
            clear()


def main():
    if platform == "linux" or platform == "linux2":
        mainLinux()
    elif platform == "Windows":
        mainWin()
    else:
        print("Not aviable yet.")
        sys.exit(1)


if __name__ == "__main__":
    main()

# :3
