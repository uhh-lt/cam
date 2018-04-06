import csv

def calculateLabel(winnerTreshold, scoreA, scoreB):
    tresholdLabel = ''
    if scoreA > scoreB:
        if (scoreB/scoreA) < winnerTreshold:
            tresholdLabel = 'BETTER'
    elif scoreA < scoreB:
        if (scoreA/scoreB) < winnerTreshold:
            tresholdLabel = 'WORSE'

    if tresholdLabel == '':
        tresholdLabel = 'NONE'
    
    return tresholdLabel

def loadFromCSV(fileName):
    listCSV = []
    with open(fileName, newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            listCSV.append(row)
    listCSV.pop(0)
    return listCSV

def main():
    print('Start evaluating:')

    requestedLabels = loadFromCSV('./csv/requested_labels.csv')
    preprocessed = loadFromCSV('./csv/preprocessed_dataset.csv')
    objectList2 = [['object_a', 'object_b', 'requested_label', 'gold_label']]

    rightCount = 0
    wrongCount = 0
    i = 0
    for pair in requestedLabels:
        goldLabel = preprocessed[i][2]
        requestedLabel = calculateLabel(WINNER_TRESHOLD, float(pair[2]), float(pair[3]))
        objectList2.append([pair[0], pair[1], requestedLabel, goldLabel])

        if requestedLabel == goldLabel:
            rightCount += 1
        else:
            wrongCount += 1

        i += 1

    with open('./csv/evaluated_with_t_' + str(WINNER_TRESHOLD) + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(objectList2)

    print('with ' + str(WINNER_TRESHOLD) + ' as treshold:')
    print('wrong: ' + str(wrongCount) + ' vs. right: ' + str(rightCount))
    print(str(rightCount*100/(rightCount+wrongCount)) + '% were right')


WINNER_TRESHOLD = 0.1
main()

