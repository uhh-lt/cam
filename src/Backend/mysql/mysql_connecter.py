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

DB_NAME = 'cam_aspects.db'
create_ratings_table_sql = ("CREATE TABLE `ratings` ("
                            "`ratingno` int NOT NULL AUTO_INCREMENT,"
                            " `aspect` text NOT NULL,"
                            " `rating` int NOT NULL,"
                            " `obja` text NOT NULL,"
                            " `objb` text NOT NULL,"
                            " PRIMARY KEY (`ratingno`)"
                            ") ENGINE=InnoDB")
create_pairs_table_sql = ("CREATE TABLE `pairs` ("
                          " `obja` text NOT NULL,"
                          " `objb` text NOT NULL,"
                          " `amount` int NOT NULL,"
                          " PRIMARY KEY (`obja`, `objb`)"
                          ") ENGINE=InnoDB")


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
        user='camuser', password='campass', host='localhost:3306')
    cursor = connection.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            connection.database = DB_NAME
            create_table(cursor, create_ratings_table_sql)
            create_table(cursor, create_pairs_table_sql)
        else:
            print(err)
            exit(1)
    return connection, cursor


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def create_table(cursor, sql_command):
    try:
        print("Creating table")
        cursor.execute(sql_command)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


def insert_predefined_pairs(predefined_pairs):
    connection, cursor = get_connection()
    for pair in predefined_pairs:
        pair.sort()
        cursor.execute('INSERT INTO pairs VALUES (?,?,0)', pair)
    close_connection(connection, cursor)


def get_predefined_pairs():
    cursor = get_connection()[1]
    cursor.execute('SELECT * FROM pairs')
    return cursor.fetchall()


def insert_rating(rating: Rating):
    connection, cursor = get_connection()
    cursor.execute('INSERT INTO ratings VALUES (?,?,?,?)',
                   rating.get_value())
    raise_value_of_pair(rating.get_pair(), cursor)
    close_connection(connection, cursor)


def raise_value_of_pair(pair, cursor):
    pair.sort()
    cursor.execute('UPDATE pairs SET amount = amount + 1 WHERE obja = ? AND objb = ?', pair)


def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()
