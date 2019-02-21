from os.path import abspath, dirname

from nltk import word_tokenize

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
CONVERTED_RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/convertedratings.csv'
CONLL_FILE_NAME_TRAIN = TARGET_DIR + '/ratingresults/ratingsconlltrain.txt'
CONLL_FILE_NAME_TEST = TARGET_DIR + '/ratingresults/ratingsconlltest.txt'

BBO = 'BBO'  # Beginning of the object the aspect belongs to
IBO = 'IBO'  # Inside the object the aspect belongs to
BOO = 'BOO'  # Beginning of the object the aspect doesn't belong to
IOO = 'IOO'  # Inside the object the aspect doesn't belong to
BGA = 'BGA'  # Beginning of a good rated aspect
IGA = 'IGA'  # Inside a good rated aspect
BEA = 'BEA'  # Beginning of an even rated aspect
IEA = 'IEA'  # Inside an even rated aspect
BBA = 'BBA'  # Beginning of a bad rated aspect
IBA = 'IBA'  # Inside a bad rated aspect
O = 'O'  # Outside of all objects and aspects

SPACE = ' '
NEWLINE = '\n'


def create_conll_file():
    with open(CONVERTED_RATINGS_FILE_NAME, 'r') as csv_file:
        train_size = int(0.8 * len(csv_file))
        with open(CONLL_FILE_NAME_TRAIN, 'w') as conll_file_train:
            convert_to_conll(csv_file[:train_size], conll_file_train)
        with open(CONLL_FILE_NAME_TEST, 'w') as conll_file_test:
            convert_to_conll(csv_file[train_size:], conll_file_test)
            

def convert_to_conll(csv_file, conll_file):
    for line in csv_file:
        parts = line.lower().split(';')
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
        sentences = [sentence.replace('\n', '')
                        for sentence in parts[8:] if sentence]

        for sentence in sentences:
            tokens = word_tokenize(sentence)
            for index in range(0, len(tokens)):
                token = tokens[index]
                conll_file.write(token + SPACE)
                if equals_part(token, aspect_object) or beginning_of_part(token, aspect_object, tokens, index):
                    conll_file.write(BBO + NEWLINE)
                elif equals_part(token, other_object) or beginning_of_part(token, other_object, tokens, index):
                    conll_file.write(BOO + NEWLINE)
                elif inside_part(token, aspect_object, tokens, index):
                    conll_file.write(IBO + NEWLINE)
                elif inside_part(token, other_object, tokens, index):
                    conll_file.write(IOO + NEWLINE)
                elif equals_part(token, aspect) or beginning_of_part(token, aspect, tokens, index):
                    if rating == 'good':
                        conll_file.write(BGA + NEWLINE)
                    elif rating == 'even':
                        conll_file.write(BEA + NEWLINE)
                    else:
                        conll_file.write(BBA + NEWLINE)
                elif inside_part(token, aspect, tokens, index):
                    if rating == 'good':
                        conll_file.write(IGA + NEWLINE)
                    elif rating == 'even':
                        conll_file.write(IEA + NEWLINE)
                    else:
                        conll_file.write(IBA + NEWLINE)
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
