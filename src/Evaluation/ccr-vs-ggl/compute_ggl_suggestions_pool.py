from multiprocessing import Pool
import json
from query_ggl_suggestions import get_suggestions


def requestGglSuggestions(comparison_object):
    ggl_suggestions = get_suggestions('{} vs'.format(comparison_object))
    print(ggl_suggestions)
    data = {
        "comparison_object": comparison_object,
        "suggestions": ggl_suggestions
    }
    return data

co_ggl_suggestions_dict = {}
p = Pool(4)

<<<<<<< HEAD
for file_counter in range(0,1,1):
=======
for file_counter in range(4,471,1):
>>>>>>> 413f56534c7334783889962ccbc655d8cfa42617
    # https://github.com/dwyl/english-words
    filename = '../../Backend/create_suggestions_index/english_words/wordlist-{}.json'.format(str('%05d' % file_counter))
    with open(filename) as json_file:
        comparison_objects = json.load(json_file)
        co_ggl_suggestions_dict = p.map(requestGglSuggestions, comparison_objects)

<<<<<<< HEAD
    outfilename = './ggl-suggestions/ggl-outfile-{}-vocab.json'.format(str('%05d' % file_counter))
=======
    outfilename = './ggl-suggestions/ggl-outfile-{}.json'.format(str('%05d' % file_counter))
>>>>>>> 413f56534c7334783889962ccbc655d8cfa42617
    with open(outfilename, 'w') as outfile:
        json.dump(co_ggl_suggestions_dict, outfile)


