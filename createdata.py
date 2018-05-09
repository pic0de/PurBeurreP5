# -*- coding: utf-8 -*-
import urllib.request
import json
import os
import sys
import time
import database as db
from termcolor import colored

program_loop = True


# Setup here the user name, password and server address about you local server connection:
user_server_name = 'root'
passwd_user_server = ''
server_address = 'localhost'

# Creation of SQL connector
newdb = db.SqlRequest('', server_address, user_server_name, passwd_user_server)
conecdb = db.SqlRequest('PurBeurreDB', server_address, user_server_name, passwd_user_server)

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "Linux":
        os.system("clear")
    elif sys.platform == "darwin":
        os.system("clear")

def create_database(db_state):
    """ Option 5 - Create the database and download the categories list """
    if db_state is False:
        newdb.create_db('database.sql')
        print("\nRetour au menu...")
        time.sleep(3)
    else:
        print("\nLa base de données existe déja, retour au menu...")
        time.sleep(3)

def destroy_database(db_state):
    """ Option 4 - Delete the database """
    if db_state is True:
        newdb.delete_db()
        print("\nBase de données effacer, retour au menu...")
        time.sleep(2)
    else:
        print("\nAucune base de données, retour au menu...")
        time.sleep(2)


# Main program
while program_loop is True:
    choice = 0
    # Check if the database exist
    db_state = newdb.check_db()
    # Clear prompt
    clear_prompt()
    print("\nBienvenue sur la base de données Pur Beurre\n")
    print("Author: Youssef Ennaciri\n")

    if db_state is True:
        # Get the categories count
        categories_count = conecdb.request_db(
            "SELECT COUNT(*) FROM categories")


    print("veuillez choisir l'une des options ci-dessous:\n")
    print("1-Créer la base de données locale")
    print("2-Effacer la base de données actuelle\n")
    while choice == 0:
        choice = input("\nVotre choix (Tapez Q pour quitter): ")

        # Stop the program
        if choice.upper() == "Q":
            program_loop = False
            break

        # Check if the input is a digit and between 0 and 3
        elif choice.isdigit() == False or int(choice) >= 3 or int(choice) == 0:
            print("\nVous devez entrer un nombre entre 1 et 3\n")
            time.sleep(2)
            break

        # Run the input choice
        elif int(choice) == 1:
            create_database(db_state)
        elif int(choice) == 2:
            destroy_database(db_state)


if __name__ == '__main__':
    pass
