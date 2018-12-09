from os.path import abspath, dirname

import mysql.connector
from mysql.connector import errorcode

pre_selected_objects = [
    ['python', 'java'],
    ['php', 'javascript'],
    ['perl', 'python'],
    ['ios', 'android'],
    ['cuda', 'opencl'],
    ['bluetooth', 'ethernet'],
    ['bmw', 'toyota'],
    ['apple', 'microsoft'],
    ['gamecube', 'ps2'],
    ['milk', 'beer'],
    ['motorcycle', 'truck'],
    ['oregon', 'michigan'],
    ['pepsi', 'coca-cola'],
    ['potato', 'steak'],
    ['tennis', 'golf']
]

DB_NAME = 'cam_aspects'
create_ratings_table_sql = ("CREATE TABLE `ratings` ("
                            "`ratingno` int NOT NULL AUTO_INCREMENT,"
                            " `aspect` varchar(200) NOT NULL,"
                            " `rating` int NOT NULL,"
                            " `obja` varchar(200) NOT NULL,"
                            " `objb` varchar(200) NOT NULL,"
                            " PRIMARY KEY (`ratingno`)"
                            ") ENGINE=InnoDB")
create_pairs_table_sql = ("CREATE TABLE `pairs` ("
                          " `obja` varchar(200) NOT NULL,"
                          " `objb` varchar(200) NOT NULL,"
                          " `amount` int NOT NULL,"
                          " PRIMARY KEY (`obja`, `objb`)"
                          ") ENGINE=InnoDB")

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/ratings.csv'


class Rating:
    '''
    A single rating of an aspect
    '''

    def __init__(self, aspect: str, rating: int, obja: str, objb: str):
        self.aspect = aspect
        self.rating = rating
        self.obja = obja
        self.objb = objb

    def get_value(self):
        return [self.aspect, self.rating, self.obja, self.objb]

    def get_pair(self):
        return [self.obja, self.objb]


def get_connection():
    connection = mysql.connector.connect(
        user='root', password='cam_root_pass', host='mysql')
    cursor = connection.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except:
        create_database(connection)
        connection.database = DB_NAME
        create_table(connection, create_ratings_table_sql)
        create_table(connection, create_pairs_table_sql)
        insert_predefined_pairs(connection, pre_selected_objects)
    return connection


def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        connection.commit()
        cursor.close()
    except:
        exit(1)


def create_table(connection, sql_command):
    cursor = connection.cursor()
    cursor.execute(sql_command)
    connection.commit()
    cursor.close()


def insert_predefined_pairs(connection, predefined_pairs):
    cursor = connection.cursor()
    for pair in predefined_pairs:
        pair.sort()
        cursor.execute(
            "INSERT INTO `pairs` (`obja`,`objb`,`amount`) VALUES (%s,%s,0)", pair)
    connection.commit()
    cursor.close()


def get_predefined_pairs():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `pairs`")
    return cursor.fetchall()


def insert_rating(rating: Rating):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO `ratings` (`aspect`,`rating`,`obja`,`objb`) VALUES (%s,%s,%s,%s)",
                   rating.get_value())
    raise_value_of_pair(rating.get_pair(), cursor)
    close_connection(connection, cursor)
    export_rating(rating)


def raise_value_of_pair(pair, cursor):
    pair.sort()
    cursor.execute(
        "UPDATE pairs SET amount = amount + 1 WHERE obja = %s AND objb = %s", pair)


def export_rating(rating: Rating):
    with open(RATINGS_FILE_NAME, 'a') as target_file:
        target_file.write(';'.join([str(col) for col in rating.get_value()]) + '\n')

def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()
