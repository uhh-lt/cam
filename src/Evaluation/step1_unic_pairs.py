import csv
import operator


def extractObjects():
    '''
        Extract the objects pairs from the evaluation_dataset
    '''
    objectList = []
    with open('./csv/evaluation_dataset.csv', newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            objectList.append(
                [row[2].lower().strip(), row[3].lower().strip()])
    objectList.pop(0)
    return objectList


def getUnicPairs(comparisons):
    '''
    Searches the unic pairs. If AB and BA is contained only one of them is taken.

    @param comparisons: list of objects which are compared, many multiple times.

    @return a set containing the pairs
    '''
    unicPairs = set()

    for comparison in comparisons:
        pair = comparison[0] + ',' + comparison[1]
        reversePair = comparison[1] + ',' + comparison[0]

        if reversePair not in unicPairs:
            unicPairs.add(pair)

    return unicPairs


def main():
    '''
    Calls the functions to compute the unic pairs sorts the resulting pairs and outputs them in a file.
    '''
    comparisonList = extractObjects()
    unicPairs = [x.split(',') for x in list(getUnicPairs(comparisonList))]
    unicPairs.sort(key=operator.itemgetter(0, 1))

    with open('./csv/unic_pairs.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(unicPairs)


main()
