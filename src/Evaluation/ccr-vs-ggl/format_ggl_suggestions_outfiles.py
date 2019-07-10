import json


ggl_suggestions_array = []
for i in range(0,1,1):
    filename = './ggl-suggestions/ggl-outfile-{}.json'.format(str('%05d' % i))
    print(filename)
    with open(filename) as json_file:
        data = json.load(json_file)
        for obj in data:
            suggestionsArray = []
            comparison_object = obj["comparison_object"]
            suggestions = obj["suggestions"]
            print(suggestions)
            for suggestion in suggestions:
                if (len(suggestion[0].split(None, 2)) > 2):
                    suggestionsArray.append(suggestion[0].split(None, 2)[2])
            gglObj = {}
            gglObj["comparison_object"] = comparison_object
            gglObj["suggestions"] = suggestionsArray
            print(gglObj)
            ggl_suggestions_array.append(gglObj)

outfilename = './ggl-suggestions-formated/ggl-outfile-all.json'
with open(outfilename, 'w') as outfile:
    json.dump(ggl_suggestions_array, outfile)

        


