import json

<<<<<<< HEAD
# this is used if handeling the whole english_words.json creates problems.
# it is split in many smaller files and if it crashes not all progress is lost.

=======
>>>>>>> 413f56534c7334783889962ccbc655d8cfa42617
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
