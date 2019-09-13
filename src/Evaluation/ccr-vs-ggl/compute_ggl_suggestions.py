from query_ggl_suggestions import get_suggestions
import json


ggl_suggestions_array = []

for file_counter in range(0,1,1):
    # https://github.com/dwyl/english-words
    filename = '../../Backend/create_suggestions_index/english_words/dict-B.json'
    with open(filename) as json_file:
        comparison_objects = json.load(json_file)
        for comparison_object in comparison_objects:
            print(comparison_object)
            suggestionsArray = []
            ggl_suggestions = get_suggestions(comparison_object)
            for suggestion in ggl_suggestions:
                if (len(suggestion[0].split(None, 2)) > 2):
                    suggestionsArray.append(suggestion[0].split(None, 2)[2])
            data = {
                "comparison_object": comparison_object,
                "suggestions": suggestionsArray
            }
            print(ggl_suggestions)
            ggl_suggestions_array.append(data)

    outfilename = './ggl-suggestions/dict-B.json'
    with open(outfilename, 'w') as outfile:
        json.dump(ggl_suggestions_array, outfile)


