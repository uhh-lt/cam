from os.path import abspath, dirname

TARGET_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))
RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/ratings.csv'
CONVERTED_RATINGS_FILE_NAME = TARGET_DIR + '/ratingresults/convertedratings.csv'


def convert_exported_ratings():
    rating_dict = {}
    with open(RATINGS_FILE_NAME, 'r') as source_file:
        for line in source_file:
            aspect, rating_str, pair_str = line.split(';', 2)
            pair = pair_str.replace(';', '/')
            rating = int(rating_str)
            if pair not in rating_dict.keys():
                rating_dict[pair] = {}
            if aspect not in rating_dict[pair].keys():
                rating_dict[pair][aspect] = []
            rating_dict[pair][aspect].append(rating)

    with open(CONVERTED_RATINGS_FILE_NAME, 'w') as target_file:
        for pair in rating_dict.keys():
            rating_list = rating_dict[pair][aspect]
            good_dict = {}
            for aspect in rating_dict[pair].keys():
                good_dict[aspect] = rating_list.count(1)
            bad_dict = {}
            for aspect in rating_dict[pair].keys():
                bad_dict[aspect] = rating_list.count(0)
            average_dict = {}
            for aspect in rating_dict[pair].keys():
                average_dict[aspect] = sum(
                    rating_list) / float(len(rating_list))

            target_file.write(
                'aspects with the most GOOD ratings for ' + pair + ':\n')
            for aspect in sorted(good_dict, key=good_dict.__getitem__, reverse=True):
                target_file.write(aspect + ';' + good_dict[aspect] + '\n')
            target_file.write('\n\n')

            target_file.write(
                'aspects with the most BAD ratings for ' + pair + ':\n')
            for aspect in sorted(bad_dict, key=bad_dict.__getitem__, reverse=True):
                target_file.write(aspect + ';' + bad_dict[aspect] + '\n')
            target_file.write('\n\n')

            target_file.write('average aspect ratings for ' + pair + ':\n')
            for aspect in sorted(average_dict, key=average_dict.__getitem__, reverse=True):
                target_file.write(aspect + ';' + average_dict[aspect] + '\n')
            target_file.write('\n\n')
