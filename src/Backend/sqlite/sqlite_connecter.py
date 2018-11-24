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
    connection = sqlite3.connect('sqlitedb/cam_aspects.db')
    return connection, connection.cursor()


def close_connection(connection):
    connection.commit()
    connection.close()


def insert_rating(rating: Rating):
    connection, cursor = get_connection()
    try:
        cursor.execute('INSERT INTO ratings VALUES (?,?,?,?)',
                       rating.get_value())
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE ratings (aspect text NOT NULL, rating int
                       NOT NULL, obja text NOT NULL, objb text NOT NULL)''')
        cursor.execute('INSERT INTO ratings VALUES (?,?,?,?)',
                       rating.get_value())
    close_connection(connection)


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


def insert_predefined_pairs(predefined_pairs):
    connection, cursor = get_connection()
    for pair in predefined_pairs:
        try:
            cursor.execute('INSERT INTO pairs VALUES (?,?,0)', pair)
        except sqlite3.OperationalError:
            try:
                cursor.execute('''CREATE TABLE pairs (obja text NOT NULL, objb text
                            NOT NULL, amount int NOT NULL, PRIMARY KEY(obja, objb))''')
                cursor.execute('INSERT INTO pairs VALUES (?,?,0)', pair)
            except sqlite3.OperationalError:
                continue
    close_connection(connection)


def get_predefined_pairs():
    cursor = get_connection()[1]
    try:
        cursor.execute('SELECT * FROM pairs')
    except sqlite3.OperationalError:
        insert_predefined_pairs(pre_selected_objects)
        cursor.execute('SELECT * FROM pairs')
    return cursor.fetchall()
