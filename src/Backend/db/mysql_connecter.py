import re
from os.path import abspath, dirname

import mysql.connector

from marker_approach.object_comparer import find_winner
from db.preselected_pairs import PREDEFINED_PAIRS
from utils.es_requester import extract_sentences, request_es
from utils.sentence_clearer import clear_sentences
from utils.objects import Argument

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
CONVERTED_RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/convertedratings.csv'

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
create_sentenceexamples_table_sql = ("CREATE TABLE `sentenceexamples` ("
                                     " `obja` varchar(200) NOT NULL,"
                                     " `objb` varchar(200) NOT NULL,"
                                     " `obj` varchar(200) NOT NULL,"
                                     " `aspect` varchar(200) NOT NULL,"
                                     " `sentex1` varchar(500) NOT NULL,"
                                     " `sentex2` varchar(500) NOT NULL,"
                                     " `sentex3` varchar(500) NOT NULL,"
                                     " `sentex4` varchar(500) NOT NULL,"
                                     " `sentex5` varchar(500) NOT NULL,"
                                     " `sentex6` varchar(500) NOT NULL,"
                                     " `sentex7` varchar(500) NOT NULL,"
                                     " `sentex8` varchar(500) NOT NULL,"
                                     " `sentex9` varchar(500) NOT NULL,"
                                     " `sentex10` varchar(500) NOT NULL,"
                                     " `sentex11` varchar(500) NOT NULL,"
                                     " `sentex12` varchar(500) NOT NULL,"
                                     " `sentex13` varchar(500) NOT NULL,"
                                     " `sentex14` varchar(500) NOT NULL,"
                                     " `sentex15` varchar(500) NOT NULL,"
                                     " `sentex16` varchar(500) NOT NULL,"
                                     " `sentex17` varchar(500) NOT NULL,"
                                     " `sentex18` varchar(500) NOT NULL,"
                                     " `sentex19` varchar(500) NOT NULL,"
                                     " `sentex20` varchar(500) NOT NULL,"
                                     " PRIMARY KEY (`obja`, `objb`, `obj`, `aspect`)"
                                     ") ENGINE=InnoDB")


class Rating:
    '''
    A single rating of an aspect
    '''

    def __init__(self, aspect: str, rating: int, obja: str, objb: str, obj: str, sentex1: str, sentex2: str, sentex3: str, sentex4: str, sentex5: str):
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
        self.sentex4 = sentex4
        self.sentex5 = sentex5

    def get_value(self):
        return [self.aspect, self.rating, self.obja, self.objb, self.obj]

    def get_pair(self):
        return [self.obja, self.objb]

    def get_sentenceexamples(self):
        return [self.obja, self.objb, self.aspect, self.obj, self.sentex1, self.sentex2, self.sentex3, self.sentex4, self.sentex5]


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
        create_table(connection, create_sentenceexamples_table_sql)
        insert_predefined_pairs(connection, PREDEFINED_PAIRS)
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
    insert_sentenceexamples_after_rating(rating.get_sentenceexamples(), cursor)
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


def insert_sentenceexamples_after_rating(sentenceexamples, cursor):
    sql = "INSERT IGNORE INTO `sentenceexamples` (`obja`,`objb`,`aspect`,`obj`"
    for i in range(1, 21):
        sql += ",`sentex" + str(i) + "`"
    sql += ") VALUES "
    cursor.execute(
        sql + "(%s,%s,%s,%s,%s,%s,%s,%s,%s,'','','','','','','','','','','','','','','')", sentenceexamples)


def insert_sentenceexamples(sentenceexamples, cursor):
    sql = "INSERT IGNORE INTO `sentenceexamples` (`obja`,`objb`,`aspect`,`obj`"
    for i in range(1, 21):
        sql += ",`sentex" + str(i) + "`"
    sql += ") VALUES "
    cursor.execute(
        sql + "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", sentenceexamples)
    print(sentenceexamples, 'has been inserted')


def get_sentenceexamples():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT `obja`, `objb`, `aspect`, `obj`,`sentex1`,`sentex2`,`sentex3`,`sentex4`,`sentex5` FROM `sentenceexamples`")
    return cursor.fetchall()


def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def export_ratings():
    with open(CONVERTED_RATINGS_FILE_NAME, 'w') as target_file:
        target_file.write(
            'OBJECT A;OBJECT B;ASPECT;ASPECT BELONGS TO;MOST FREQUENT RATING;CONFIDENCE;AMOUNT OF GOOD RATINGS;AMOUNT OF BAD RATINGS; SENTENCE EXAMPLE 1; SENTENCE EXAMPLE 2; SENTENCE EXAMPLE 3; SENTENCE EXAMPLE 4; SENTENCE EXAMPLE 5\n')
        rating_dict = {}

        for rating in get_ratings():
            key = ';'.join(rating[:4])
            if key not in rating_dict.keys():
                rating_dict[key] = {}
                rating_dict[key]['ratings'] = []
            rating_dict[key]['ratings'].append(rating[4])

        for sentenceexamples in get_sentenceexamples():
            key = ';'.join(sentenceexamples[:4])
            if key in rating_dict.keys():
                sentenceexamples_str = ';'.join(sentenceexamples[4:])
                rating_dict[key]['sentenceexamples'] = sentenceexamples_str

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
                              ';' + str(good_ratings) + ';' + str(bad_ratings) + ';')
            target_file.write(
                rating_dict[aspect_key]['sentenceexamples'] + '\n')


def create_sentence_examples():
    connection = get_connection()
    cursor = connection.cursor()
    for pair in PREDEFINED_PAIRS:
        obj_a = Argument(pair[0])
        obj_b = Argument(pair[1])
        print('requesting ES with', obj_a.name, obj_b.name)
        json_compl = request_es('false', obj_a, obj_b)
        all_sentences = extract_sentences(json_compl)
        all_sentences = clear_sentences(all_sentences, obj_a, obj_b)
        if all_sentences:
            result = find_winner(all_sentences, obj_a, obj_b, [])
            for o, aspects in zip([obj_a, obj_b], [result['extractedAspectsObject1'], result['extractedAspectsObject2']]):
                for aspect in aspects:
                    sentenceexamples = [obj_a.name, obj_b.name, aspect, o.name]
                    i = 0
                    for sentence in o.sentences:
                        txt = sentence['text']
                        word_list = re.compile('\w+').findall(txt)
                        if aspect in word_list:
                            replaced_txt = txt.replace(';', ',').replace('"', '').replace('\n', '')
                            sentenceexamples.append(replaced_txt[:500])
                            i += 1
                        if i > 19:
                            break
                    while i < 20:
                        sentenceexamples.append('')
                        i += 1
                    insert_sentenceexamples(sentenceexamples, cursor)
    close_connection(connection, cursor)