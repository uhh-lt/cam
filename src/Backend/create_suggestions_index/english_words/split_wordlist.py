import json

counter = 0
data = {}
file_counter = 0

with open('english_words.json') as json_file:
    comparison_objects = json.load(json_file)
    for co in comparison_objects:
        counter += 1
        data[co] = 1
        if counter > 498:
            filename = 'wordlist-{}.json'.format(str('%05d' % file_counter))
            with open(filename, 'w') as outfile:
                json.dump(data, outfile)
            counter = 0
            data = {}
            file_counter += 1
