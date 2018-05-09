# -*- coding: utf-8 -*-

import urllib.request
import json

import pymysql.cursors

class SqlRequest:
    '''Communication with the SQL datbase.
       Create the class with database name, host address of the server,
       user name and password access'''

    def __init__(self, db_name, host_address, user_name, password):
        '''Class initialisator'''
        self.db_name = db_name
        self.host_address = host_address
        self.user_name = user_name
        self.password = password

    def create_db(self, filename):
        ''' Function to create and download the database'''

        try:
            self.db_connect = pymysql.connect(host=self.host_address,
                                              user=self.user_name, password=self.password,
                                              database=self.db_name, charset='utf8')
            cursor = self.db_connect.cursor()
            # Open SQL file
            with open(filename, 'r') as fileToRead:
                sqlFile = fileToRead.read()

            # split all command by ';'
            sqlCommand = sqlFile.split(';')

            # Execute each command in sqlcommand
            for command in sqlCommand:
                try:
                    if command.strip() != '':
                        cursor.execute(command)
                except pymysql.err.InternalError as msg:
                        print("Erreur: {}".format(msg))
            print("\nBase de données créer")
            print("\nChargement de la base de données...")

            # Get the french categorie database from OpenFoodFacts and add to the local database
            categories_url = urllib.request.urlopen('https://fr.openfoodfacts.org/categories.json')
            data = categories_url.read()
            json_output = json.loads(data.decode("UTF-8"))

            # Change the type to str format, control len size and take of the langage prefixe(Cleaning file)
            for categorie in json_output["tags"]:
                cat_name = categorie['name']
                cat_name = cat_name.replace("'", " ")
                if (len(cat_name) >= 76) or (len(categorie['url']) >= 151):
                    continue
                if cat_name[2:3] == ":":
                    continue
                if len(cat_name) == 0:
                    continue
                data = (cat_name, categorie['url'])

                # Insert into the categories table
                cursor.execute("INSERT IGNORE INTO categories (cat_name, cat_url) VALUES ('{}', '{}')".format(
                    cat_name, categorie['url']))
                self.db_connect.commit()

            # Get the total number of the categories table and print
            cursor.execute("SELECT COUNT(*) FROM categories")
            self.sql_message = cursor.fetchone()
            print("Base de données chargé avec %s produits" % (self.sql_message))

        except Exception as e:
            print("Erreur : %s" % e)

    def delete_db(self):
        '''Delete the database'''

        try:
            self.db_connect = pymysql.connect(host=self.host_address,
                                              user=self.user_name, password=self.password,
                                              database=self.db_name, charset='utf8')
            cursor = self.db_connect.cursor()
            cursor.execute("DROP DATABASE IF EXISTS PurBeurreDB;")
            self.db_connect.commit()

        except Exception as e:
            print("Erreur : %s" % e)

    def request_db(self, request_db, multi_results = False):
        '''Request to the database, this function return the answer if not null
           Add the SQL command in parameter, use multi_results=True for a list answer
           (by default False => single answer)'''
        self.sql_message = ''
        try:
            # Connect to the database
            self.db_connect = pymysql.connect(host=self.host_address,
                                              user=self.user_name, password=self.password,
                                              database=self.db_name, charset='utf8')
            cursor = self.db_connect.cursor()
            cursor.execute(request_db)
            self.db_connect.commit()
            if multi_results is True:
                self.sql_message = [item for item in cursor.fetchall()]
            else:
                self.sql_message = cursor.fetchone()
                self.sql_message = self.sql_message[0]
            return self.sql_message

        except Exception as e:
            return e

    def check_db(self):
        """ Check if the database exist """
        state = False
        # Connect to the database
        self.db_connect= pymysql.connect(host=self.host_address,
                                         user=self.user_name, password=self.password,
                                         database=self.db_name, charset='utf8')
        cursor = self.db_connect.cursor()
        database = ("SHOW DATABASES")
        cursor.execute(database)
        for database in cursor:
            database = database[0]
            if str(database) == "PurBeurreDB":
                state = True
                break
            else:
                state = False
        return state

    def cat_search_db(self, name_search):
        """ Return a search of 10 items """
        self.db_connect = pymysql.connect(host=self.host_address,
                                          user=self.user_name, password=self.password,
                                          database=self.db_name, charset='utf8')

        cursor = self.db_connect.cursor()
        result = ("SELECT cat_name, cat_id FROM categories WHERE cat_name LIKE '{}%' LIMIT 10".format(name_search))
        cursor.execute(result)
        results = [item for item in cursor.fetchall()]
        return results

    def product_show_db(self, cat_id):
        """ Show the product table """
        results = list()
        self.db_connect = pymysql.connect(host=self.host_address,
                                          user=self.user_name, password=self.password,
                                          database=self.db_name, charset='utf8')

        cursor = self.db_connect.cursor()
        request = ("""SELECT pro_id, pro_name FROM product WHERE pro_cat_id = {} ORDER BY pro_id""".format(cat_id))
        cursor.execute(request)
        results = [item for item in cursor.fetchall()]
        return results

    def product_db(self, categorie_name):
        """ Get the product list from the categorie """
        try:
            self.db_connect = pymysql.connect(host=self.host_address,
                                              user=self.user_name, password=self.password,
                                              database=self.db_name, charset='utf8')

            # Get the product list from the selected categorie
            cursor = self.db_connect.cursor()
            cursor.execute("SELECT cat_url, cat_id FROM categories WHERE cat_name LIKE '{}'".format(categorie_name))
            result = cursor.fetchone()
            url_product_list, cat_product_list = result
            url_product_list += ".json"
            product_url = urllib.request.urlopen(url_product_list)
            data = product_url.read()
            json_output = json.loads(data.decode("utf_8"))

            # Get information from the product list
            for product in json_output['products']:
                if len(product['product_name_fr']) > 76:
                    continue
                product_name = product['product_name_fr']
                product_name = product_name.replace("'", ' ')
                if 'stores' in product:
                    product_shop = str(product['stores'])
                    product_shop = product_shop.replace(' ', '-')
                    if product_shop is "":
                        product_shop = ("Inconnu")
                else:
                    product_shop = ("Inconnu")
                product_url = product['url']
                nutr_sco = product['nutrition_score_debug']

                # Try the id_nutrition score number if is a dozen or unit number
                try:
                    int(nutr_sco[len(nutr_sco)-2])
                    nutrition_score = nutr_sco[len(nutr_sco)-2]+nutr_sco[len(nutr_sco)-1]
                except:
                    nutrition_score = nutr_sco[len(nutr_sco)-1]
                if nutrition_score.isdigit() is True:
                    nutrition_score = int(nutrition_score)
                else:
                    nutrition_score = 0

                # Insert into the categories table
                cursor.execute("""INSERT INTO product
                    (pro_name, pro_shop, pro_url, pro_nutriscore, pro_cat_id)
                    VALUES ('%s', '%s', '%s', %d, %d)
                    ON DUPLICATE KEY UPDATE pro_name = '%s'""" %
                    (product_name, product_shop, product_url, nutrition_score, cat_product_list, product_name))
                self.db_connect.commit()

        except Exception as e:
            print("Erreur : %s" % e)

if __name__ == '__main__':
    # Test
    newdb = SqlRequest('PurBeurreDB', 'localhost', 'root', '')
    resultat = newdb.cat_search_db('Boeuf')
    print(resultat[1][1])
