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
    # s_rem = re.sub('[^a-zA-Z0-9 ]', ' ', sentence)
    s_rem = sentence
    # find all words in the sentence
    wordlist = word_tokenize(s_rem)
    taglist = nltk.pos_tag(wordlist)
    return taglist


def collectAspectsPerTriple(objectList):
    pairSentences = {}

    for objects in objectList:
        objectA = objects[0]
        objectB = objects[1]
        label = objects[2]
        sentence = objects[3]
        pair = objectA + ',' + objectB + ',' + label
        inversePair = objectB + ',' + objectA + ',' + buildInverseLabel(label)

        if pair in pairSentences and inversePair not in pairSentences:
            pairSentences[pair].update(
                generateAspects(sentence, objectA, objectB))
        elif pair not in pairSentences and inversePair in pairSentences:
            pairSentences[inversePair].update(
                generateAspects(sentence, objectA, objectB))
        else:
            pairSentences[pair] = set()
            pairSentences[pair].update(
                generateAspects(sentence, objectA, objectB))

    return pairSentences


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

    tripleAspects = collectAspectsPerTriple(objectList)
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

    triples.sort(key=operator.itemgetter(0, 1))
    triples.insert(0, header)

    with open('./csv/preprocessed_dataset.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(triples)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
