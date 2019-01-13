from os.path import abspath, dirname

import mysql.connector
from mysql.connector import errorcode
import re

from marker_approach.object_comparer import find_winner
from utils.es_requester import extract_sentences, request_es
from utils.sentence_clearer import clear_sentences

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
CONVERTED_RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/convertedratings.csv'

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
                            " `obj` varchar(200) NOT NULL,"
                            " PRIMARY KEY (`ratingno`)"
                            ") ENGINE=InnoDB")
create_pairs_table_sql = ("CREATE TABLE `pairs` ("
                          " `obja` varchar(200) NOT NULL,"
                          " `objb` varchar(200) NOT NULL,"
                          " `amount` int NOT NULL,"
                          " PRIMARY KEY (`obja`, `objb`)"
                          ") ENGINE=InnoDB")
create_sentexs_table_sql = ("CREATE TABLE `sentexs` ("
                            " `obja` varchar(200) NOT NULL,"
                            " `objb` varchar(200) NOT NULL,"
                            " `obj` varchar(200) NOT NULL,"
                            " `aspect` varchar(200) NOT NULL,"
                            " `sentex1` varchar(2000) NOT NULL,"
                            " `sentex2` varchar(2000) NOT NULL,"
                            " `sentex3` varchar(2000) NOT NULL,"
                            " PRIMARY KEY (`obja`, `objb`, `obj`, `aspect`)"
                            ") ENGINE=InnoDB")


class Rating:
    '''
    A single rating of an aspect
    '''

    def __init__(self, aspect: str, rating: int, obja: str, objb: str, obj: str, sentex1: str, sentex2: str, sentex3: str):
        self.aspect = aspect
        self.rating = rating
        pairs = [obja, objb]
        pairs.sort()
        self.obja = pairs[0]
        self.objb = pairs[1]
        self.obj = obj
        self.sentex1 = sentex1
        self.sentex2 = sentex2
        self.sentex3 = sentex3

    def get_value(self):
        return [self.aspect, self.rating, self.obja, self.objb, self.obj]

    def get_pair(self):
        return [self.obja, self.objb]

    def get_sentexs(self):
        return [self.obja, self.objb, self.aspect, self.obj, self.sentex1, self.sentex2, self.sentex3]


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
        create_table(connection, create_sentexs_table_sql)
        insert_predefined_pairs(connection, pre_selected_objects)
        insert_predefined_pairs(connection, read_predefined_pairs_from_file())
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
            "INSERT IGNORE INTO `pairs` (`obja`,`objb`,`amount`) VALUES (%s,%s,0)", pair)
    connection.commit()
    cursor.close()


def read_predefined_pairs_from_file():
    predefined_pairs = []

    with open(dirname(abspath(__file__)) + 'pairs.csv', 'r') as source:
        for line in source:
            predefined_pairs.append(line.split(';', 1))

    return predefined_pairs


def get_predefined_pairs():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `pairs`")
    return cursor.fetchall()


def insert_rating(rating: Rating):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO `ratings` (`aspect`,`rating`,`obja`,`objb`,`obj`) VALUES (%s,%s,%s,%s,%s)",
                   rating.get_value())
    raise_value_of_pair(rating.get_pair(), cursor)
    insert_sentexs(rating.get_sentexs(), cursor)
    close_connection(connection, cursor)


def get_ratings():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT `obja`, `objb`, `aspect`, `obj`, `rating` FROM `ratings`")
    return cursor.fetchall()


def raise_value_of_pair(pair, cursor):
    cursor.execute(
        "UPDATE pairs SET amount = amount + 1 WHERE obja = %s AND objb = %s", pair)


def insert_sentexs(sentexs, cursor):
    cursor.execute(
        "INSERT IGNORE INTO `sentexs` (`obja`,`objb`,`aspect`,`obj`,`sentex1`,`sentex2`,`sentex3`) VALUES (%s,%s,%s,%s,%s,%s,%s)", sentexs)


def get_sentexs():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT `obja`, `objb`, `aspect`, `obj`,`sentex1`,`sentex2`,`sentex3` FROM `sentexs`")
    return cursor.fetchall()


def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def export_ratings():
    with open(CONVERTED_RATINGS_FILE_NAME, 'w') as target_file:
        target_file.write(
            'OBJECT A;OBJECT B;ASPECT;ASPECT BELONGS TO;MOST FREQUENT RATING;CONFIDENCE;AMOUNT OF GOOD RATINGS;AMOUNT OF BAD RATINGS; SENTENCE EXAMPLE 1; SENTENCE EXAMPLE 2; SENTENCE EXAMPLE 3\n')
        rating_dict = {}

        for rating in get_ratings():
            key = ';'.join(rating[:4])
            if key not in rating_dict.keys():
                rating_dict[key] = {}
                rating_dict[key]['ratings'] = []
            rating_dict[key]['ratings'].append(rating[4])

        for sentexs in get_sentexs():
            key = ';'.join(sentexs[:4])
            sentexs_str = ';'.join(sentexs[4:7])
            rating_dict[key]['sentexs'] = sentexs_str

        for aspect_key in rating_dict.keys():
            target_file.write(aspect_key + ';')

            good_ratings = rating_dict[aspect_key]['ratings'].count(1)
            bad_ratings = rating_dict[aspect_key]['ratings'].count(0)

            if good_ratings > bad_ratings:
                most_frequent_rating = 'GOOD'
                confidence = good_ratings / \
                    float(good_ratings + bad_ratings)
            elif bad_ratings > good_ratings:
                most_frequent_rating = 'BAD'
                confidence = bad_ratings / \
                    float(good_ratings + bad_ratings)
            else:
                most_frequent_rating = 'EVEN'
                confidence = good_ratings / \
                    float(good_ratings + bad_ratings)

            target_file.write(most_frequent_rating + ';' + str(confidence) +
                              ';' + str(good_ratings) + ';' + str(bad_ratings))
            target_file.write(rating_dict[aspect_key]['sentexs'] + '\n')
