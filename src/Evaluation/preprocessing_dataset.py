import csv
import operator
import re
import nltk
from nltk import word_tokenize
import time


def extractData():
    objectList = []
    with open('./csv/evaluation_dataset.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            objectList.append(
                [row[2].lower().strip(), row[3].lower().strip(), row[9].strip(), row[17]])
    objectList.pop(0)
    return objectList


def tag_sentence(sentence):
    '''
    Returns a list of tags for each word of the sentence. A tag is a combination of the word and
    its part of speech coded as an NLTK tag, for example ('apple', 'NN').
    '''
    # remove special characters
    s_rem = re.sub('[^a-zA-Z0-9 ]', ' ', sentence)
    # find all words in the sentence
    wordlist = word_tokenize(s_rem)
    taglist = nltk.pos_tag(wordlist)
    return taglist


def collectAspectsPerTriple(objectList):
    tripleSentences = {}
    pairs = set()

    for objects in objectList:
        objectA = objects[0]
        objectB = objects[1]
        label = objects[2]
        sentence = objects[3]

        pair = objectA + ',' + objectB
        inversePair = objectB + ',' + objectA
        triple = pair + ',' + label
        inverseTriple = inversePair + ',' + buildInverseLabel(label)

        aspects = generateAspects(sentence, objectA, objectB)

        if triple in tripleSentences:
            tripleSentences[triple].update(aspects)
        elif inverseTriple in tripleSentences:
            tripleSentences[inverseTriple].update(aspects)
        elif pair in pairs:
            tripleSentences[triple] = set(aspects)
        elif inversePair in pairs:
            tripleSentences[inverseTriple] = set(aspects)
        else:
            pairs.add(pair)
            tripleSentences[triple] = set(aspects)

    return [tripleSentences, pairs]


def filterCommonAspects(listA, listB, listC):
    listA = list(set(listA).difference(listB))
    return list(set(listA).difference(listC))


def buildInverseLabel(label):
    if label == 'BETTER':
        label = 'WORSE'
    elif label == 'WORSE':
        label = 'BETTER'
    return label


def generateAspects(sentence, objectA, objectB):
    taglist = tag_sentence(sentence)
    aspects = []
    for tag in taglist:
        possibleAspect = tag[0].lower()
        if tag[1].startswith('NN') and possibleAspect != objectA and possibleAspect != objectB:
            aspects.append(possibleAspect)

    return aspects


def main():
    objectList = extractData()

    triplesAndPairs = collectAspectsPerTriple(objectList)
    tripleAspects = triplesAndPairs[0]
    pairs = triplesAndPairs[1]

    print(len(pairs))
    for pair in pairs:
        betterTriple = pair + ',BETTER'
        worseTriple = pair + ',WORSE'
        noneTriple = pair + ',NONE'
        betterAspects = tripleAspects[betterTriple] if betterTriple in tripleAspects else []
        worseAspects = tripleAspects[worseTriple] if worseTriple in tripleAspects else []
        noneAspects = tripleAspects[noneTriple] if noneTriple in tripleAspects else []

        if betterTriple in tripleAspects:
            tripleAspects[betterTriple]  = filterCommonAspects(betterAspects, worseAspects, noneAspects)
        if worseTriple in tripleAspects:
            tripleAspects[worseTriple] = filterCommonAspects(worseAspects, betterAspects, noneAspects)
        if noneTriple in tripleAspects:
            tripleAspects[noneTriple] = filterCommonAspects(noneAspects, worseAspects, betterAspects)

    triples = []
    header = ['object_a', 'object_b', 'label']
    maxAspects = 0
    for triple, aspects in tripleAspects.items():
        numberOfAspects = len(aspects)
        # if numberOfAspects == 0:      # Filter out trible with no aspects
        #     print(triple)
        #     continue
        if maxAspects < numberOfAspects:
            maxAspects = numberOfAspects
        triples.append([x for x in triple.split(',')])
        triples[len(triples)-1].extend(aspects)

    for i in range(0, maxAspects, 1):
        header.append('aspect_' + str(i))

    triples.sort(key=operator.itemgetter(0, 1, 2))
    triples.insert(0, header)

    with open('./csv/preprocessed_dataset.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(triples)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
