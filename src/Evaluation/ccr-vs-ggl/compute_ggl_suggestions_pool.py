from multiprocessing import Pool
import json
from query_ggl_suggestions import get_suggestions


def requestGglSuggestions(comparison_object):
    ggl_suggestions = get_suggestions('{} vs'.format(comparison_object))
    print(ggl_suggestions)
    for suggestion in ggl_suggestions:
    if (len(suggestion[0].split(None, 2)) > 2):
        suggestionsArray.append(suggestion[0].split(None, 2)[2])

    data = {
        "comparison_object": comparison_object,
        "suggestions": suggestionsArray
    }
    return data

co_ggl_suggestions_dict = {}
p = Pool(4)

# https://github.com/dwyl/english-words = dict-A
filename = '../../Backend/create_suggestions_index/english_words/dict-A.json'
with open(filename) as json_file:
    comparison_objects = json.load(json_file)
    co_ggl_suggestions_dict = p.map(requestGglSuggestions, comparison_objects)

outfilename = './ggl-suggestions/ggl-suggestions-dict-A.json'
with open(outfilename, 'w') as outfile:
    json.dump(co_ggl_suggestions_dict, outfile)


