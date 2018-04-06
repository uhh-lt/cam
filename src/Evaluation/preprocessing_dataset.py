import csv
import operator


def extractData():
    objectList = []
    with open('./csv/evaluation_dataset.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            objectList.append(
                [row[2].lower().strip(), row[3].lower().strip(), row[9].strip()])
    objectList.pop(0)
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
    pairs = []

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

        maximum = max(betterCount, worseCount, nonCount)
        label = ''
        if betterCount == maximum:
            label = 'BETTER'
        elif worseCount == maximum:
            label = 'WORSE'
        else:
            label = 'NONE'

        objects = [x for x in pair.split(',')]
        pairs.append([objects[0], objects[1], label,
                      betterCount, worseCount, nonCount], )

    return pairs


def main():
    objectList = extractData()
    pairsCounts = countUnicPairLabels(objectList)
    pairs = calculateLabel(pairsCounts)

    pairs.sort(key=operator.itemgetter(0))
    pairs.insert(0, ['object_a', 'object_b', 'label',
                     'BETTER_count', 'WORSE_count', 'NONE_count'])

    with open('./csv/preprocessed_dataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(pairs)


main()
