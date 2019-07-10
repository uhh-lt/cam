import requests
import csv
import time
import threading
import math
import sys
sys.path.append('../../Backend')
import es_requester
from sentence_clearer import clear_sentences
from main import Argument


class myThread (threading.Thread):
    def __init__(self, threadID, name, pairs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pairs = pairs
        self.resultList = []

    def run(self):
        print("Starting " + self.name)
        self.resultList = self.requestSentences(self.pairs, self.name)
        print("Finished " + self.name)

    def requestSentences(self, pairs, threadName):
        '''
        Builds the urls and calls the function to request.
        Uses the functions of the Backend to extract and clear the sentences:
        'extract_sentences' and 'clear_sentences'

        @param pairs: all unic pairs extracted from file

        @param threadName: name of the thread

        @returns list of results, an entry per pair which consists of the pair itself,
        the requested sentences and the corresponding scores of the sentences
        '''
        resultList = []
        urls = buildURLs(pairs)

        for i in range(0, len(urls), 1):
            objectA = pairs[i][0]
            objectB = pairs[i][1]
            jsonResult = self.sendRequest(urls[i])
            allSentences = es_requester.extract_sentences(jsonResult)
            allSentences = clear_sentences(
                allSentences, Argument(objectA), Argument(objectB))

            sentences = []
            scores = []

            for key in allSentences:
                sentences.append(key)
                scores.append(allSentences[key])

            resultList.append([objectA, objectB])
            resultList[len(resultList)-1].extend(sentences)
            resultList[len(resultList)-1].extend(scores)

        return resultList

    def sendRequest(self, url):
        '''
        Trys to get the given url, if an error occures the function itself
        is called again to try it another time.

        @param url: which is requested

        @returns the json result of the request
        '''
        try:
            jsonResult = requests.get(url)

            return jsonResult
        except requests.exceptions.RequestException:
            print('Pair raised an exception, trying again.')
            return self.sendRequest(url)


def buildURLs(pairs):
    '''
    Builds a list of urls using the Backend functions 'build_object_urlpart' and 'add_marker_urlpart'

    @param pairs: all unic pairs

    @return list of len(pairs) urls
    '''
    urls = []
    for pair in pairs:
        objectA = Argument(pair[0])
        objectB = Argument(pair[1])
        url = es_requester.build_object_urlpart(objectA, objectB)
        url = es_requester.add_marker_urlpart(url, 'false')
        urls.append(url)

    return urls


def main():
    '''
    Starts the threads to request the sentences for the unic pairs faster.
    In the end the pairs and corresponding sentences with scores are written to a file.
    '''
    pairs = []
    with open('./csv/step1_unic_pairs.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            pairs.append(row)

    # *****Threads here*****
    # Create new threads
    threads = []

    numberOfThreads = 30
    i = math.ceil(len(pairs)/numberOfThreads)

    for j in range(0, numberOfThreads, 1):
        threads.append(myThread(j, "Thread-" + str(j), pairs[(j*i):((j+1)*i)]))

    # Start new Threads
    for t in threads:
        t.start()

    print('Processing...')
    # Wait for all threads to complete
    for t in threads:
        while(t.isAlive()):
            pass

    requested = []
    for t in threads:
        print('Wait')
        t.join()
        requested.extend(t.resultList)

    print("Exiting Main Thread")
    print(str(len(requested)) + ' results.')
    # **********************

    with open('./csv/step2_requested_sentences.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(requested)

    print("Exiting Main Thread")
    # **********************


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
