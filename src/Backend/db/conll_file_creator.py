from os.path import abspath, dirname
from random import shuffle

from nltk import word_tokenize, pos_tag

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
CONVERTED_RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/convertedratings.csv'
CONLL_FILE_NAME_TRAIN = TARGET_DIR + '/ratingresults/ratingsconlltrain.txt'
CONLL_FILE_NAME_TEST = TARGET_DIR + '/ratingresults/ratingsconlltest.txt'
CONLL_FILE_NAME_DEV = TARGET_DIR + '/ratingresults/ratingsconlldev.txt'

BBO = 'B-ASPOBJ'  # Beginning of the object the aspect belongs to
IBO = 'I-ASPOBJ'  # Inside the object the aspect belongs to
BOO = 'B-OTHOBJ'  # Beginning of the object the aspect doesn't belong to
IOO = 'I-OTHOBJ'  # Inside the object the aspect doesn't belong to
BGA = 'B-ASP'  # Beginning of an aspect
IGA = 'I-ASP'  # Inside an aspect
O = 'O'  # Outside of all objects and aspects

SPACE = ' '
NEWLINE = '\n'


class Sentence:
    def __init__(self, aspect_object: str, other_object: str, aspect: str, rating: str, text: str):
        self.aspect_object = aspect_object
        self.other_object = other_object
        self.aspect = aspect
        self.rating = rating
        self.text = text


def create_conll_file():
    with open(CONVERTED_RATINGS_FILE_NAME, 'r') as csv_file:
        content = [line.strip().lower().split(';') for line in csv_file.readlines()]
        sentence_list = []
        for parts in content:
            if len(parts) < 9:
                continue
            first_object = parts[0]
            if 'object a' in first_object:
                continue
            second_object = parts[1]
            aspect = parts[2]
            aspect_object = parts[3]
            if first_object == aspect_object:
                other_object = second_object
            else:
                other_object = first_object
            rating = parts[4]
            sentences = [sentence for sentence in parts[8:] if sentence]

            for sentence in sentences:
                sentence_list.append(Sentence(aspect_object, other_object, aspect, rating, sentence))

        shuffle(sentence_list)
        train_size = int(0.75 * len(sentence_list))
        test_size = int(0.15 * len(sentence_list))
        with open(CONLL_FILE_NAME_TRAIN, 'w') as conll_file_train:
            convert_to_conll(sentence_list[:train_size], conll_file_train)
        with open(CONLL_FILE_NAME_TEST, 'w') as conll_file_test:
            convert_to_conll(sentence_list[train_size:train_size + test_size], conll_file_test)
        with open(CONLL_FILE_NAME_DEV, 'w') as conll_file_dev:
            convert_to_conll(sentence_list[train_size + test_size:], conll_file_dev)
            

def convert_to_conll(sentence_list, conll_file):
    for sentence in sentence_list:
        tokens = word_tokenize(sentence.text)
        for index in range(0, len(tokens)):
            token = tokens[index]
            conll_file.write(token + SPACE)
            if equals_part(token, sentence.aspect_object) or beginning_of_part(token, sentence.aspect_object, tokens, index):
                conll_file.write(BBO + NEWLINE)
            elif equals_part(token, sentence.other_object) or beginning_of_part(token, sentence.other_object, tokens, index):
                conll_file.write(BOO + NEWLINE)
            elif inside_part(token, sentence.aspect_object, tokens, index):
                conll_file.write(IBO + NEWLINE)
            elif inside_part(token, sentence.other_object, tokens, index):
                conll_file.write(IOO + NEWLINE)
            elif equals_part(token, sentence.aspect) or beginning_of_part(token, sentence.aspect, tokens, index):
                if sentence.rating == 'good':
                    conll_file.write(BGA + NEWLINE)
            elif inside_part(token, sentence.aspect, tokens, index):
                if sentence.rating == 'good':
                    conll_file.write(IGA + NEWLINE)
            else:
                conll_file.write(O + NEWLINE)
        conll_file.write(NEWLINE)


def equals_part(token, part):
    return token == part


def beginning_of_part(token, part, tokens, index):
    if part.startswith(token) and len(part) > len(token):
        expanding_token = token
        i = 1
        while index + i < len(tokens):
            expanding_token += SPACE + tokens[index + i]
            if equals_part(expanding_token, part):
                return True
            if not part.startswith(expanding_token):
                return False
            if not len(part) > len(expanding_token):
                return False
            i += 1
    return False


def inside_part(token, part, tokens, index):
    if token in part:
        expanding_token = token
        i = 1
        while part.find(expanding_token) > 0 and index - i >= 0:
            expanding_token = tokens[index - i] + SPACE + expanding_token
            if equals_part(expanding_token, part):
                return True
            if beginning_of_part(expanding_token, part, tokens, index):
                return True
            if not expanding_token in part:
                return False
            i += 1
    return False
