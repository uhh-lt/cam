from query_ggl_suggestions import get_suggestions
import json


co_ggl_suggestions_dict = []

for file_counter in range(0,1,1):
    # https://github.com/dwyl/english-words
    filename = '../../Backend/create_suggestions_index/english_words/wordlist-{}.json'.format(str('%05d' % file_counter))
    with open(filename) as json_file:
        comparison_objects = json.load(json_file)
        for comparison_object in comparison_objects:
            print(comparison_object)
            ggl_suggestions = get_suggestions(comparison_object)
            data = {
                "comparison_object": comparison_object,
                "suggestions": ggl_suggestions
            }
            print(ggl_suggestions)
            co_ggl_suggestions_dict.append(data)

    outfilename = './ggl-suggestions/ggl-outfile-{}.json'.format(str('%05d' % file_counter))
    with open(outfilename, 'w') as outfile:
        json.dump(co_ggl_suggestions_dict, outfile)


