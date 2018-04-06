import requests
import csv
import operator
import time

def buildURL(objA, objB, aspectMap, model, fastSearch):
    hostname = ''
    if model == 'default':
        hostname = 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
    elif model == 'machine_learning':
        hostname = 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
    URL = hostname + '?fs=' + fastSearch + '&objectA=' + objA + '&objectB=' + objB
    URL += addAspectURL(aspectMap)
    return URL


def addAspectURL(aspectMap):
    url_part = ''
    i = 1
    for k, v in aspectMap.items():
        url_part += '&aspect' + i + '=' + k + '&weight' + i+1 + '=' + v
        i += 1
    return url_part


def requestLabels(url, objects):
    jsonResult = requests.get(url)

    scoreA = jsonResult.json()['score object 1']
    scoreB = jsonResult.json()['score object 2']
   
    return [objects[0], objects[1], scoreA, scoreB]

def main():
    pairs = []
    with open('./csv/preprocessed_dataset.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            pairs.append(row)
    pairs.pop(0)

    requested = [['object_a', 'object_b', 'score_a', 'score_b']]

    for objects in pairs:
        url = buildURL(objects[0], objects[1], dict(), 'default', 'false')
        result = requestLabels(url, objects)
        print(result[0] + ' ' +  result[1] + ' ' + str(result[2]) + ' ' + str(result[3]))
        requested.append(result)

    with open('./csv/requested_labels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(requested)

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))