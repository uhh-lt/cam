import csv
import time
import math
import sys
from random import shuffle
from operator import itemgetter
import threading
sys.path.append('../Backend')
from object_comparer import find_winner
from main import Aspect
from main import Argument


class myThread (threading.Thread):
    def __init__(self, threadID, name, preprocessed, pairsSentences):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.preprocessed = preprocessed
        self.pairsSentences = pairsSentences
        self.resultList = []

    def run(self):
        print("Starting " + self.name)
        self.resultList = self.calculateWinner(
            self.preprocessed, self.pairsSentences)
        print("Finished " + self.name)

    def calculateWinner(self, preprocessed, pairsSentences):
        '''
        Goes through the assigned preprocessed comparisons, reads the aspects 
        and calls a Backend function (find_winner) to compute the scores of the given pair 
        with respect to the aspects

        @param preprocessed: the preprocessed comparisons

        @param pairsSentences: a dictionary where the sentences of a pair can be
        accessed by the pair as key

        @returns a list containing the computed scores  ['id', 'object_a', 'object_b',
                  'gold_label', 'score_a', 'score_b']
        '''
        resultList = []
        for comparison in preprocessed:
            result = comparison[:4]
            objectA = comparison[1]
            objectB = comparison[2]
            pair = objectA + "," + objectB
            reversedPair = objectB + "," + objectA

            tempAspects = [x for x in comparison[5].split(', ')]
            aspects = [Aspect(aspect, 5) for aspect in tempAspects]

            sentences = pairsSentences[pair] if pair in pairsSentences else pairsSentences[
                reversedPair] if reversedPair in pairsSentences else {}
            finalDict = find_winner(sentences, Argument(
                objectA), Argument(objectB), aspects)

            scoreA = finalDict['score object 1']
            scoreB = finalDict['score object 2']

            print(result[0])

            result.extend([scoreA, scoreB])
            resultList.append(result)
        return resultList


def loadFromCSV(fileName):
    '''
    Loads all rows of the given url to a csv file and returns it
    '''
    listCSV = []
    with open(fileName, mode='r', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            listCSV.append(row)
    return listCSV


def extractPairSentences(requestedSentences):
    '''
    Builds a dictionary to access the sentences of the pairs easily

    @param requestedSentences: a list which contains the objects, 
    the corresponding sentences and the scores of the sentences

    @returns a dictionary with the pairs as key and the corresponding sentences -> score dic 
    as value
    '''
    pairsSentences = {}
    for sentencesOfPair in requestedSentences:
        sentenceOffset = int((len(sentencesOfPair) - 2) / 2) + 2
        allSentences = {}
        objectA = sentencesOfPair[0]
        objectB = sentencesOfPair[1]
        pair = objectA + "," + objectB
        sentences = sentencesOfPair[2:sentenceOffset]
        scores = sentencesOfPair[sentenceOffset:]
        for i in range(0, len(sentences), 1):
            allSentences[sentences[i]] = float(scores[i])
        pairsSentences[pair] = allSentences

    return pairsSentences


def main():
    '''
    Reads in the needed files to compute the scores for the pairs and starts
    up numberOfThreads threads to calculate the scores concurrently
    '''
    print('Start evaluating:')
    urlParam = 'related'
    requestedSentences = loadFromCSV('./csv/step2_requested_sentences.csv')
    preprocessed = loadFromCSV(
        './csv/({})_preprocessed_dataset.csv'.format(urlParam))
    preprocessed.pop(0)
    pairsSentences = extractPairSentences(requestedSentences)

    shuffle(preprocessed)
    numberOfThreads = 72
    i = math.ceil(len(preprocessed)/numberOfThreads)
    threads = []
    for j in range(0, numberOfThreads, 1):
        threads.append(myThread(j, "Thread-" + str(j),
                                preprocessed[(j*i):((j+1)*i)], pairsSentences))

    # Start new Threads
    for t in threads:
        t.start()

    print('Processing...')
    # Wait for all threads to complete
    for t in threads:
        while(t.isAlive()):
            pass

    requested = [['id', 'object_a', 'object_b',
                  'gold_label', 'score_a', 'score_b']]
    resultList = []
    for t in threads:
        resultList.extend(t.resultList)
    resultList.sort(key =lambda x: int(itemgetter(0)(x)))
    requested.extend(resultList)
    
    with open('./csv/({})_requested_labels.csv'.format(urlParam), 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(requested)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
