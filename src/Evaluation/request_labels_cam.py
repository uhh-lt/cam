import requests
import csv
import operator
import time
import threading
import math


class myThread (threading.Thread):
    def __init__(self, threadID, name, comparations):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.comparations = comparations
        self.resultList = []

    def run(self):
        print("Starting " + self.name)
        self.resultList = self.executeComparision(self.comparations, self.name)
        print("Finished " + self.name)

    def requestLabels(self, url, id):
        try:
            jsonResult = requests.get(url).json()
            scoreA = jsonResult['score object 1']
            scoreB = jsonResult['score object 2']

            return [scoreA, scoreB]
        except requests.exceptions.RequestException:
            print('Pair with id {}, raised an exception'.format(id))
            return self.requestLabels(url, id)

    def executeComparision(self, comparations, threadName):
        urls = generateURLS(comparations)
        resultList = []
        for i in range(0, len(urls), 1):
            id = comparations[i][0]
            result = comparations[i][:4]
            result.extend(self.requestLabels(urls[i], id))
            resultList.append(result)
            print(result[0] + ' ' + result[1] + ' ' + result[2] + ' ' +
                  result[3] + ' ' + str(result[4]) + ' ' + str(result[5]))
            # print(url)

        return resultList


def buildURL(objA, objB, aspectMap, model, fastSearch):
    hostname = ''
    if model == 'default':
        hostname = 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
        # hostname = 'http://127.0.0.1:5000/cam'
    elif model == 'machine_learning':
        hostname = 'http://ltdemos.informatik.uni-hamburg.de/cam-api'
        # hostname = 'http://127.0.0.1:5000/cam'
    URL = hostname + '?fs=' + fastSearch + '&objectA=' + objA + '&objectB=' + objB
    URL += addAspectURL(aspectMap)
    return URL


def addAspectURL(aspectMap):
    url_part = ''
    i = 1
    for k, v in aspectMap.items():
        url_part += '&aspect' + str(i) + '=' + k + \
            '&weight' + str(i) + '=' + str(v)
        i += 1
    return url_part


def generateURLS(comparations):
    urls = []
    for objects in comparations:
        aspects = [x for x in objects[5].split(', ')]
        aspectDict = {}
        for aspect in aspects:
            aspectDict[aspect] = 5
        urls.append(buildURL(objects[1], objects[2],
                             aspectDict, 'default', 'false'))
    return urls


def main():
    comparations = []
    urlParam = 'NN+JJ'
    with open('./csv/({})_preprocessed_dataset.csv'.format(urlParam), newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            comparations.append(row)
    comparations.pop(0)

    requested = [['id', 'object_a', 'object_b',
                  'gold_label', 'score_a', 'score_b']]

    # *****Threads here*****
    # Create new threads

    numberOfThreads = 20
    i = math.ceil(len(comparations)/numberOfThreads)
    threads = []
    for j in range(0, numberOfThreads, 1):
        threads.append(myThread(j, "Thread-" + str(j),
                                comparations[(j*i):((j+1)*i)]))

    # Start new Threads
    for t in threads:
        t.start()

    print('Processing...')
    # Wait for all threads to complete
    for t in threads:
        while(t.isAlive()):
            pass

    for t in threads:
        print('Wait')
        t.join()
        requested.extend(t.resultList)

    print("Exiting Main Thread")
    print(str(len(requested)) + ' results.')
    # **********************

    with open('./csv/({})_requested_labels.csv'.format(urlParam), 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(requested)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
