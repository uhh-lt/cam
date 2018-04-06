import csv
import requests
import json


WINNER_TRESHOLD = 0.8

def extractData():
    objectList = []
    with open('evaluation_dataset.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            objectList.append(
                [row[2].lower().strip(), row[3].lower().strip(), row[9].strip()])
    objectList.pop(0)

    # with open('objects.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(objectList)

    return objectList


def countUnicPairLabels(objectList):

    unicPairs = set()
    betterPairCount = {}
    worsePairCount = {}
    nonePairCount = {}

    for objects in objectList:
        pair = objects[0] + ',' + objects[1]
        unicPairs.add(pair)

        if objects[2] == 'BETTER':
            count(betterPairCount, pair)
        elif objects[2] == 'WORSE':
            count(worsePairCount, pair)
        else:
            count(nonePairCount, pair)

    return [unicPairs, betterPairCount, worsePairCount, nonePairCount]


def count(pairs, pair):
    if pair in pairs:
        pairs[pair] += 1
    else:
        pairs[pair] = 1
    return pairs


def calculateLabel(pairsCounts):
    objectList = []
    for pair in pairsCounts[0]:
        betterCount = 0
        worseCount = 0
        nonCount = 0

        if pair in pairsCounts[1]:
            betterCount = pairsCounts[1][pair]
        if pair in pairsCounts[2]:
            worseCount = pairsCounts[2][pair]
        if pair in pairsCounts[3]:
            nonCount = pairsCounts[3][pair]

        print(str(betterCount) + ' ' + str(worseCount) + ' ' + str(nonCount))
        maximum = max(betterCount, worseCount, nonCount)
        print('max: ' + str(maximum))
        label = ''
        if betterCount == maximum:
            label = 'BETTER'
        elif worseCount == maximum:
            label = 'WORSE'
        else:
            label = 'NONE'

        print(pair + ' ' + label)
        objects = [x for x in pair.split(',')]
        objectList.append([objects[0], objects[1], label])

    with open('objects.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(objectList)
    return objectList


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
    print(url)
    jsonResult = requests.get(url)

    scoreA = jsonResult.json()['score object 1']
    scoreB = jsonResult.json()['score object 2']
    winner = jsonResult.json()['winner'].lower().strip()

    # TODO: Treshold for better or worse label -> ~20% higher score to win
    
    tresholdLabel = ''
    if scoreA > scoreB:
        if (scoreB/scoreA) < WINNER_TRESHOLD:
            tresholdLabel = 'BETTER'
    elif scoreA < scoreB:
        if (scoreA/scoreB) < WINNER_TRESHOLD:
            tresholdLabel = 'WORSE'

    if tresholdLabel == '':
        tresholdLabel = 'NONE'
    
    absoluteLabel = ''
    if winner == objects[0]:
        absoluteLabel = 'BETTER'
    elif winner == objects[1]:
        absoluteLabel = 'WORSE'
    elif winner == 'no winner found':
        absoluteLabel = 'NONE'

    print(tresholdLabel + ' vs. ' + absoluteLabel)

    return [objects[0], objects[1], tresholdLabel, objects[2], scoreA, scoreB]


def main():
    print('Start evaluating:')

    objectList = extractData()
    pairsCounts = countUnicPairLabels(objectList)
    objectList = calculateLabel(pairsCounts)

    objectList2 = [['objectA', 'objectB',
                    'requestedLabel', 'goldLabel', 'scoreA', 'scoreB']]

    rightCount = 0
    wrongCount = 0
    i = 500
    for objects in objectList:
        url = buildURL(objects[0], objects[1], dict(), 'default', 'false')
        result = requestLabels(url, objects)
        objectList2.append(result)

        if result[2] == objects[2]:
            rightCount += 1
        else:
            wrongCount += 1

        print([objects[0] + ' vs. ' + objects[1] +
               ' -> ' + result[2] + ' == ' + objects[2]])

        if i == 0:
            break
        else:
            i -= 1

    with open('RequestedLabels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(objectList2)

    print('wrong: ' + str(wrongCount) + ' vs. right: ' + str(rightCount))
    print(str(rightCount*100/(rightCount+wrongCount)) + '% were right')


main()
