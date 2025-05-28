import json
import time
from pathlib import Path
import sys


def type_print(msg, speed=0.03):
    for ch in msg:
        print(ch, end='', flush=True)
        time.sleep(speed)

greet= "Welcome back, Master! Your digital vault awaits your command. Choose an option from below list :\n1. Access your existing passwords\n2. Save a new password\n3. Edit any existing password\n4. Delete any existing password\n5. Exit\n\n"


database = Path(__file__).parent/"database.json"
def load_data():
    global data
    try :
        with open(database, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError,FileNotFoundError):
        data = {} 
#Dependencies for Menu 3rd
def main_menu():
    while True:
        type_print(greet,0.01)
        load_data()
        choice=input("--> Enter your command: ")
        
        if choice == "1":
            show_passwords()
        elif choice == "2":
            add_password()
        elif choice == "3":
            edit_password()
        elif choice == "4":
            del_password()
        elif choice == "5":
            type_print("Closing the vault... Stay safe!\n")
            sys.exit()
        else:
            type_print("Invalid choice. Try again.\n")


def show_passwords():    
    if not data :
        type_print("Vault is Empty, Master !")
        return
    else :
        type_print("Here is all of your passwords :\n")
        for key, value in data.items():
            website, username = key.split("_")
            type_print(f"Password of {username}'s {website} account is : {value}\n\n")
        type_print('Going back to main menu...\n')
        return

def add_password():
    a = input("Enter the website name : ")
    b = input("Enter your username : ")
    c = input("Enter the password to save : ")

    data[f"{a}_{b}"] = c

    with open(database,"w") as f:
        json.dump(data, f, indent=4)

    type_print("Saving changes...\n")
    type_print("Vault closed securely. Opening main menu...\n")
    return

def edit_password() :
    if not data:
        type_print("Vault is empty")
        return
    else :
        temp_data = {}
        for i, (key, value) in enumerate(data.items(), start=1):
            temp_data[f"key_{i}"] = key
            a,b = key.split("_") 
            type_print(f"{i}. {a}'s {b} account password -> {value}\n")
        number = input("Enter the serial number of the account you want to edit :")

        while True :

            fstring= f"key_{number}"
            key_in_process = temp_data.get(fstring)
            if key_in_process :
                a1, b1 = key_in_process.split("_")
                new_pass = input(f"Okay enter new password for {b1}'s {a1} account: " )
                data[key_in_process] = new_pass

                with open(database,"w") as f:
                    json.dump(data, f, indent=4)

                type_print("Saving changes...\n")
                type_print("Vault closed securely. Opening main menu...\n")
                return
            else:
                type_print("The given input is not an valid number, please retry with a valid response\n")
                number=input("--> ")

def del_password() :
    if not data:
        type_print("Vault is empty")
        return
    else :
        temp_data = {}
        for i, (key, value) in enumerate(data.items(), start=1):
            temp_data[f"key_{i}"] = key
            a,b = key.split("_") 
            type_print(f"{i}. {a}'s {b} account password -> {value}\n")
        number = input("Enter the serial number of the account you want to delete :")

        while True :

            fstring= f"key_{number}"
            key_in_process = temp_data.get(fstring)
            if key_in_process :
                data.pop(key_in_process)

                with open(database,"w") as f:
                    json.dump(data, f, indent=4)

                type_print("Saving changes...\n")
                type_print("Vault closed securely. Opening main menu...\n")
                return
            else:
                type_print("The given input is not an valid number, please retry with a valid response\n")
                number=input("--> ")                
            

    
if __name__ == "__main__":
    main_menu()
