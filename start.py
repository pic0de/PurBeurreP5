# coding: utf-8

import urllib.request
import json
import os
import sys
import time

import database as db

program_loop = True


# Setup here the user name, password and server address about you local server connection:
user_server_name = 'root'
passwd_user_server = ''
server_address = 'localhost'

# Creation of SQL connector
newdb = db.SqlRequest('', server_address, user_server_name, passwd_user_server)
conecdb = db.SqlRequest('dbopenfoodfacts', server_address, user_server_name, passwd_user_server)

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "win32":
        os.system("cls")
    elif sys.platform == "Linux":
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

def create_user(db_state):
    """ Create a user account """
    if db_state is True:
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous créer un utilisateur ? O/n ")
            if choice.upper() == "N":
                break

            elif choice.upper() == "O":
                user_name = input("Nom d'utilisateur: ")

                # Insert the user name in the user table
                user = conecdb.request_db(
                    "INSERT INTO user (user_name) VALUES ('%s')" % user_name, True)

                if not user:
                    print("Nom d'utilisateur créer, retour au menu...")
                else:
                    print("Utilisateur déjà enregistré, retour au menu...")
                time.sleep(2)
                break
            else:
                choice = 0
    else:
        print("\nVeuillez créer la base de données, retour au menu...")
        time.sleep(2)

def access_sav(db_state, user_count):
    """Show the saved product in saved table """
    # If the DB exist
    if db_state is True:
        if user_count is not 0:
            choice = 0
            while choice is 0:

                # Request to the DB for user list
                user_list = conecdb.request_db(
                    "SELECT * FROM user ORDER BY user_id", True)
                choice = input("\nVoulez vous afficher les produits sauvegardés ? O/n ")
                if choice.upper() == "N":
                    break
                elif choice.upper() == "O":
                    user_choice = 0
                    user_id = []
                    while user_choice is 0:
                        print("\nVoici le(s) utilisateur(s) enregistré\n")
                        for num, user in user_list:
                            print("{} - {}".format(num, user))
                            user_id.append(num)
                        user_choice = input("\nSélectionné l'utilisateur à afficher: ")
                        if user_choice.isdigit():
                            if int(user_choice) in user_id:

                                # Request on the DB of the sav list of user
                                user_sav = conecdb.request_db(
                                    """SELECT  product.pro_name, product.pro_shop, product.pro_url,
                                       categories.cat_name FROM product
                                       LEFT JOIN saved ON saved.sav_pro_id = product.pro_id
                                       LEFT JOIN categories ON categories.cat_id = product.pro_cat_id
                                       WHERE saved.sav_User_id = {}""".format(user_choice), True)

                                # If user doesn't have saved product
                                if not user_sav:
                                    print("Cet utilisateur n'a aucun produit sauvegardé, retour au menu...")
                                    time.sleep(2)
                                    break

                                # Print the result of the user saved
                                product_count = 0
                                for item in user_sav:
                                    print("\n*****************************************")
                                    print("Produit {}:".format(product_count + 1))
                                    print("Le produit {} appartient à la catégorie {}.".format(
                                        item[0], item[3]))
                                    if item[1] == "Inconnu":
                                        print("Il n'y a pas de magasin connu pour ce produit")
                                    else:
                                        print("On peut trouver ce produit chez {}".format(item[1]))
                                    print("Voici le lien URL du produit: {}".format(item[2]))
                                    print("*****************************************")
                                    product_count += 1
                                print("Appuyez sur une touche pour revenir au menu...")
                                break_time = os.popen("pause")
                                break_time.read()
                                break
                            else:
                                print("\nChoix incorrect ")
                                choice = 0
                        else:
                            print("\nChoix incorrect, veuillez entrer un chiffre correspondant à la liste\n")
                            time.sleep(2)
                            user_choice = 0
                else:
                    choice = 0
        else:
            print("\nIl n'y a aucun utilisateur enregistré, retour au menu...")
            time.sleep(2)
    else:
        print("\nIl n'y a pas de base de données créer, retour au menu...")
        time.sleep(2)

def search_product(db_state, user_count):
    """ Search a product in categories list """
    # If the DB exist
    if db_state is True:
        choice = 0
        while choice is 0:

            # Check count of user in DB
            if user_count is 0:
                print("\nAttention ! Il n'y a pas de compte utilisateur créer pour sauvegarder")
            choice = input("\nVoulez vous rechercher un produit ? O/n ")
            if choice.upper() == "N":
                break
            elif choice.upper() == "O":
                search_loop = 0

                # Search categorie
                while search_loop is 0:
                    categorie = input("\nEntrez le début du nom de la catégorie: ")
                    print("")

                    # Request DB for categories
                    results = conecdb.cat_search_db(str(categorie))
                    if len(results) == 0 :
                            print("Aucun résultat")
                            continue

                    number_list = 0
                    for item, number in results:
                        print("{} - {}".format(number_list, item))
                        number_list += 1
                    print("\nEntrez le numéro correspondant à votre recherche,")
                    cat_choice = input("Tapez Q pour quitter ou n'importe quel lettre pour relancer une recherche: ")

                    # Check if the product list of choice is already download
                    if cat_choice.isdigit() and int(cat_choice) >=0 and int(cat_choice) <= 9:
                        product_count = conecdb.request_db(
                            "SELECT COUNT(*) FROM `product` WHERE `pro_cat_id` = {}".format(results[int(cat_choice)][1]))
                        if product_count == 0:
                            print("Chargement en cours...")
                            conecdb.product_db(results[int(cat_choice)][0])
                    else:
                        if cat_choice.upper() == "Q":
                            print("Retour au menu...")
                            time.sleep(3)
                            break
                        else:
                            print("\nChoix incorrect, retour à la recherche...\n")
                            time.sleep(2)
                            continue

                    # Show the product list
                    product_list = conecdb.product_show_db(results[int(cat_choice)][1])

                    if not product_list:
                        print("Aucun produit trouver dans la categorie, retour au menu...")
                        time.sleep(2)
                        break

                    # Select the product in the list
                    print("\nVoici une selection de produit dans la catégorie {} :".format(results[int(cat_choice)][0]))
                    number_list = 0
                    for pro_id, pro_name in product_list:
                        print(str(number_list) + " - " + pro_name)
                        number_list += 1
                    product_choice = input("\nQuel produit voulez vous consulter ? (Q pour revenir au menu) ")
                    if product_choice.isdigit():
                        if int(product_choice) >=0 and int(product_choice) <= len(product_list):
                            product_choice = product_list[int(product_choice)][0]

                            # Request the product table for the product description by join the categories table
                            product_sql = conecdb.request_db("""SELECT
                                categories.cat_name, product.pro_name, product.pro_shop,
                                product.pro_url, product.pro_nutriscore
                                FROM categories INNER JOIN product
                                ON categories.cat_id = product.pro_cat_id
                                WHERE product.pro_id = '{}'""".format(product_choice), True)
                            product = product_sql[0]


                            # Request the product table for better nutrition score
                            pro_better_score = conecdb.request_db(
                                """SELECT pro_name, pro_nutriscore, pro_id FROM product
                                WHERE product.pro_nutriscore > {} AND product.pro_cat_id = {}""".format(product[4], results[int(cat_choice)][1]), True)

                            # Print the result of the search product
                            print("\n*****************************************")
                            print("\nLe produit {} appartient à la catégorie {}.".format(product[1], product[0]))
                            if product[2] == "Inconnu":
                                print("Il possède un score nutritionnel de {}, il n'y a aucun magasin connu pour l'acheter.".format(product[4]))
                            else:
                                print("Il possède un score nutritionnel de {}, vous pouvez le trouver chez {}.".format(product[4], product[2]))
                            print("Voici le lien URL du produit : {}".format(product[3]))
                            print("\n*****************************************")
                            if not pro_better_score :
                                print("\nIl n'y a aucun produit avec un meilleur score nutritionnel dans cette catégorie")
                            else:
                                number_list = 0
                                for product, score, pro_nuti_id in pro_better_score:
                                    print("{} - Le produit {} a un meilleur score nutritionnel avec un score de {}.".format(number_list, product, score))
                                    number_list += 1
                                print("")

                            # Save the product
                            if user_count == 0:
                                print("Impossible de sauvegarder le produit, il n'y a pas de compte utilisateur")
                                print("Appuyez sur une touche pour revenir au menu...")
                                break_time = os.popen("pause")
                                break_time.read()
                                break
                            elif not pro_better_score:
                                print("Impossible de sauvegarder le produit, il n'y a pas de substitution")
                                print("Appuyez sur une touche pour revenir au menu...")
                                break_time = os.popen("pause")
                                break_time.read()
                                break
                            else:
                                save_choice = 0
                                while save_choice is 0:
                                    save_choice = input("Voulez vous sauvegarder le produit ? O/n ")
                                    print("")

                                    # Get the user on the DB
                                    if save_choice.upper() == "O":
                                        user = conecdb.request_db(
                                            "SELECT * FROM user ORDER BY user_id", True)
                                        for id, user_name in user:
                                            print("{} - {}".format(id, user_name))
                                        user_choice = 0
                                        while user_choice is 0:
                                            user_choice = input("\nQuelle utilisateur voulez-vous utiliser ? ")
                                            if user_choice.isdigit() >= 1 and user_choice.isdigit() <= len(user):
                                                user_choice = int(user_choice)

                                                # Insertion of product in saved table
                                                substitution = input("Entrer le numéro du substitut à sauvegarder: ")
                                                if substitution.isdigit() and int(substitution) <= (len(pro_better_score)-1):
                                                    substitution = pro_better_score[int(substitution)][2]
                                                    conecdb.request_db("""INSERT INTO saved (sav_pro_id, sav_user_id)
                                                                        SELECT product.pro_id, user.User_id
                                                                        FROM user, product
                                                                        WHERE product.pro_id = {} AND user.User_id = {}""".format(substitution, user_choice))
                                                    print("Produit sauvegardé, retour au menu...")
                                                    time.sleep(2)
                                                    search_loop = 1
                                                else:
                                                    print("Choix incorrect, veuillez recommencer.")
                                                    user_choice = 0
                                            elif user_choice.upper() == "Q":
                                                print("Retour au menu...")
                                                time.sleep(2)
                                                break
                                            else:
                                                print("Choix incorrect, veuillez recommencer.")
                                    elif save_choice.upper() == "N":
                                        print("\nRetour au menu...")
                                        time.sleep(2)
                                        break
                                    else:
                                        print("\nChoix incorrect")
                                        save_choice = 0
                        else:
                            print("Choix incorrect, retour à la recherche...")
                            time.sleep(2)
                            continue
                    elif product_choice.upper() == "Q":
                        print("Retour au menu...")
                        time.sleep(2)
                        break
                    else:
                        print("Choix incorrect, retour à la recherche...")
                        time.sleep(2)
                        continue
            else:
                choice = 0
    else:
        print("\nVeuillez créer la base de données, retour au menu...")
        time.sleep(2)

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
    user_count = 0
    categories_count = 0
    # Check if the database exist
    db_state = newdb.check_db()
    # Clear prompt
    clear_prompt()
    print("\nPure Beurre Product Search:")
    print("")

    if db_state is True:
        # Get the user count
        user_count = conecdb.request_db("SELECT COUNT(*) FROM user")
        # Get the categories count
        categories_count = conecdb.request_db(
            "SELECT COUNT(*) FROM categories")
        if user_count is 0:
            print("Veuillez créer un compte utilisateur pour pouvoir sauvegarder un produit")
        else:
            print("Il y a %s utilisateur(s) enregistré(s) dans la base de données." % user_count)
        print("La base de données possède actuellement %s categories" % categories_count)
    else:
        print("Il n'y a aucune base de données actuellement")

    print("************************************************\n")
    print("1-Créer la base de données locale")
    print("2-Créer un compte utilisateur")
    print("3-Accédez à vos produits sauvegardés")
    print("4-Rechercher un produit dans la listes des catégories")
    print("5-Effacer la base de données actuelle")
    while choice == 0:
        choice = input("\nVotre choix (Tapez Q pour quitter): ")

        # Stop the program
        if choice.upper() == "Q":
            program_loop = False
            break

        # Check if the input is a digit and between 0 and 6
        elif choice.isdigit() == False or int(choice) >= 6 or int(choice) == 0:
            print("\nVous devez entrer un nombre entre 1 et 5\n")
            time.sleep(2)
            break

        # Run the input choice
        elif int(choice) == 1:
            create_database(db_state)
        elif int(choice) == 2:
            create_user(db_state)
        elif int(choice) == 3:
            access_sav(db_state, user_count)
        elif int(choice) == 4:
            search_product(db_state, user_count)
        elif int(choice) == 5:
            destroy_database(db_state)


if __name__ == '__main__':
    pass
