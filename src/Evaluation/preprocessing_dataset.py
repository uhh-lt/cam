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

def generateAspects(sentence, objectA, objectB):
    taglist = tag_sentence(sentence)
    aspects = set()
    for tag in taglist:
        possibleAspect = tag[0].lower()
        if tag[1].startswith('NN') and possibleAspect != objectA and possibleAspect != objectB:
            aspects.add(possibleAspect)

    return aspects

def collectAspectsPerSentence(comparisonList):
    header = ['object_a', 'object_b', 'label']
    sentences = []
    maxAspects = 0
    for comparation in comparisonList:
        objectA = comparation[0]
        objectB = comparation[1]
        label = comparation[2]
        sentence = comparation[3]

        sentences.append([objectA, objectB, label])
        aspects = generateAspects(sentence, objectA, objectB)

        numberOfAspects = len(aspects)
        if maxAspects < numberOfAspects:
            maxAspects = numberOfAspects

        sentences[len(sentences)-1].extend(aspects)

    for i in range(0, maxAspects, 1):
        header.append('aspect_' + str(i))

    sentences.sort(key=operator.itemgetter(0, 1, 2))
    sentences.insert(0, header)
    return sentences
    


def main():
    comparisonList = extractData()
    comparationsWithAspects = collectAspectsPerSentence(comparisonList)


    with open('./csv/preprocessed_dataset.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(comparationsWithAspects)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
