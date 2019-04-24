from multiprocessing import Pool
import requests
import time
import json
#from sample_wordlist import comparison_objects
#from sample_wordlist import comparison_objects_small



CCR_BASE_URL = "http://127.0.0.1:5000/ccr/"

co_suggestions_dict = {}

def requestSuggestions(comparison_object):
    ccr_suggestions = requests.get(CCR_BASE_URL + '{}'.format(comparison_object)).json()
    data = {
        "comparison_object": comparison_object,
        "suggestions": ccr_suggestions
        }
    
    return data

p = Pool(4)

with open('english_words_sample.json') as json_file:
    comparison_objects = json.load(json_file)
    co_suggestions_dict = p.map(requestSuggestions, comparison_objects)

with open('co_suggestions_dict.txt', 'w') as outfile:
    json.dump(co_suggestions_dict, outfile)

#print(co_suggestions_dict)

