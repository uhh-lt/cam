import csv
import operator
import nltk
from nltk import word_tokenize
import time
import sys
sys.path.append('../Backend')
import link_extracter
import constants


def extractData():
    '''
    Extraxts needed data of the evaluation dataset csv file and returns it as list.

    @returns list [objecta, objectb, goldlabel, sentence]

    '''
    objectList = []
    with open('./csv/evaluation_dataset.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            objectList.append(
                [row[2].lower().strip(), row[3].lower().strip(), row[9].strip(), row[17]])
    objectList.pop(0)
    return objectList


def generateAspects(sentence, objectA, objectB):
    '''
    Generates aspects of the given sentence. If aspects are object a oder b they are filtered out.

    @returns a list of generated aspects
    '''
    taglist = link_extracter.tag_sentence(sentence)
    aspects = set()
    for tag in taglist:
        possibleAspect = tag[0].lower()
        if (tag[1].startswith('JJ') or tag[1].startswith('NN')) and possibleAspect != objectA and possibleAspect != objectB \
                and possibleAspect not in constants.STOPWORDS and possibleAspect not in constants.NUMBER_STRINGS and len(possibleAspect) > 1:
            aspects.add(possibleAspect)

    return aspects


def collectAspectsPerSentence(comparisonList):
    '''
    Builds up the preprocessed dataset, basically adding the generated aspects to each comparison

    @param comparisonList: contains the extracted data containing the objects, the gold label and the sentence

    @returns a list containing an id, the objects, the gold label, the sentence and the generated aspects
    '''
    header = ['id', 'object_a', 'object_b', 'label', 'sentence', 'aspects']
    comparisonAspects = []
    for comp in comparisonList:
        objectA = comp[0]
        objectB = comp[1]
        label = comp[2]
        sentence = comp[3]

        comparisonAspects.append([objectA, objectB, label, sentence])
        aspects = generateAspects(sentence, objectA, objectB)
        aspects = list(aspects)
        aspects.sort()
        comparisonAspects[len(comparisonAspects)-1].append(", ".join(aspects))

    comparisonAspects.sort(key=operator.itemgetter(0, 1, 2))
    comparisonAspects.insert(0, header)

    for i in range(1, len(comparisonAspects), 1):
        comparisonAspects[i].insert(0, i)

    return comparisonAspects


def main():
    '''
    Calls all methods to generate aspects and align them to the sentences. In the end the list 
    is printed to a csv file.
    '''
    comparisonList = extractData()
    comparisonList.sort(key=operator.itemgetter(0, 1, 2))
    comparationsWithAspects = collectAspectsPerSentence(comparisonList)
    urlParam = '-'
    with open('./csv/({})preprocessed_dataset.csv'.format(urlParam), 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(comparationsWithAspects)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
