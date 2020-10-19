import json
import time
from multiprocessing import Pool

import requests

# from sample_wordlist import comparison_objects
# from sample_wordlist import comparison_objects_small


CCR_BASE_URL = "http://127.0.0.1:5000/ccr/"

# co_suggestions_dict = {}
co_suggestions = []


def requestSuggestions(comparison_object):
    ccr_suggestions = requests.get(CCR_BASE_URL + '{}'.format(comparison_object)).json()
    data = {
        "comparison_object": comparison_object,
        "suggestions": ccr_suggestions
    }

    return data


p = Pool(4)
start = time.time()

for file_counter in range(0, 1, 1):
    # https://github.com/dwyl/english-words
    filename = './english_words/wordlist-{}.json'.format(str('%05d' % file_counter))
    with open(filename) as json_file:
        comparison_objects = json.load(json_file)
        # co_suggestions_dict = p.map(requestSuggestions, comparison_objects)

        for comparison_object in comparison_objects:
            ccr_suggestions = requests.get(CCR_BASE_URL + '{}'.format(comparison_object)).json()
            data = {
                "comparison_object": comparison_object,
                "suggestions": ccr_suggestions
            }
            co_suggestions.append(data)

    outfilename = './suggestions/outfile-{}.json'.format(str('%05d' % file_counter))
    with open(outfilename, 'w') as outfile:
        # json.dump(co_suggestions_dict, outfile)
        json.dump(co_suggestions, outfile)

end = time.time()
print('took: ', end - start)
