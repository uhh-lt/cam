import random
from os.path import abspath, dirname

from utils.es_requester import extract_sentences, request_es
from utils.objects import Argument
from utils.sentence_clearer import clear_sentences

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/ratings.csv'
CONVERTED_RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/convertedratings.csv'


def convert_exported_ratings():
    rating_dict = {}
    with open(RATINGS_FILE_NAME, 'r') as source_file:
        for line in source_file:
            aspect, rating_str, pair_str = line.split(';', 2)
            pair = pair_str.replace(';', '///')
            rating = int(rating_str)
            if pair not in rating_dict.keys():
                rating_dict[pair] = {}
            if aspect not in rating_dict[pair].keys():
                rating_dict[pair][aspect] = []
            rating_dict[pair][aspect].append(rating)

    with open(CONVERTED_RATINGS_FILE_NAME, 'w') as target_file:
        target_file.write(
            'object_a;object_b;aspect;most_frequent_rating;confidence;good_ratings;bad_ratings;example_sentence_1;example_sentence_2;example_sentence_3')

        for pair in rating_dict.keys():
            object_a, object_b = pair.split('///', 1)

            obj_a = Argument(object_a)
            obj_b = Argument(object_b)

            json_compl = request_es('false', obj_a, obj_b)
            all_sentences = extract_sentences(json_compl)
            all_sentences = clear_sentences(all_sentences, obj_a, obj_b)

            target_file.write(object_a + ';' + object_b + ';')

            for aspect in rating_dict[pair].keys():
                target_file.write(aspect + ';')

                good_ratings = rating_dict[pair][aspect].count(1)
                bad_ratings = rating_dict[pair][aspect].count(0)

                if good_ratings > bad_ratings:
                    most_frequent_rating = 'good'
                    confidence = good_ratings / \
                        float(good_ratings + bad_ratings)
                else:
                    most_frequent_rating = 'bad'
                    confidence = bad_ratings / \
                        float(good_ratings + bad_ratings)

                target_file.write(most_frequent_rating + ';' + str(confidence) +
                                  ';' + str(good_ratings) + ';' + str(bad_ratings) + ';')

                aspect_sentences = [
                    sentence for sentence in all_sentences if aspect in sentence]
                chosen_sentences = random.sample(
                    aspect_sentences, min(3, len(aspect_sentences)))

                example_sentence_1 = ''
                example_sentence_2 = ''
                example_sentence_3 = ''
                if len(chosen_sentences) > 0:
                    example_sentence_1 = chosen_sentences[0]
                    if len(chosen_sentences) > 1:
                        example_sentence_2 = chosen_sentences[1]
                        if len(chosen_sentences) > 2:
                            example_sentence_3 = chosen_sentences[2]
                target_file.write(
                    example_sentence_1 + ';' + example_sentence_2 + ';' + example_sentence_3 + '\n')
