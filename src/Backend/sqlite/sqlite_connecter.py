import sqlite3


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
        return [self.aspect, self.rating, self.obja, self.objb, ]


def get_connection():
    #connection = sqlite3.connect('/srv/docker/pan-cam3/src/Backend/sqlite/cam_aspects.db')
    connection = sqlite3.connect('cam_aspects.db')
    return connection, connection.cursor()


def close_connection(connection):
    connection.commit()
    connection.close()


def create_db():
    connection, cursor = get_connection()
    cursor.execute('''CREATE TABLE ratings (aspect text NOT NULL, rating int
                   NOT NULL, obja text NOT NULL, objb text NOT NULL)''')
    close_connection(connection)


def insert_rating(rating: Rating):
    connection, cursor = get_connection()
    try:
        cursor.execute('INSERT INTO ratings VALUES (?,?,?,?)', rating.get_value())
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE ratings (aspect text NOT NULL, rating int
                       NOT NULL, obja text NOT NULL, objb text NOT NULL)''')
        cursor.execute('INSERT INTO ratings VALUES (?,?,?,?)', rating.get_value())
    close_connection(connection)


def get_connection_path():
    connection, cursor = get_connection()
    cursor.execute("PRAGMA database_list")
    rows = cursor.fetchall()
    for row in rows:
        return row[2]