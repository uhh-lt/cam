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

    for i in range(1, 11, 1):
        treshold = 0.1*i
        totalRight = 0
        totalWrong = 0

        betterTP = 0
        betterFP = 0
        betterTN = 0
        betterFN = 0

        worseTP = 0
        worseFP = 0
        worseTN = 0
        worseFN = 0

        noneTP = 0
        noneFP = 0
        noneTN = 0
        noneFN = 0

        index = 0
        for pair in requestedLabels:
            goldLabel = preprocessed[index][2]
            requestedLabel = calculateLabel(
                treshold, float(pair[2]), float(pair[3]))
            objectList2.append([pair[0], pair[1], requestedLabel, goldLabel])


            if requestedLabel == goldLabel:
                totalRight += 1
                if requestedLabel == 'BETTER':
                    betterTP += 1
                elif requestedLabel == 'WORSE':
                    worseTP += 1
                else:
                    noneTP += 1
            else:
                totalWrong += 1
                if requestedLabel == 'BETTER':
                    betterFP += 1
                elif requestedLabel == 'WORSE':
                    worseFP += 1
                else:
                    noneFP += 1

            if goldLabel != 'BETTER' and requestedLabel != 'BETTER':
                betterTN += 1
            if goldLabel != 'WORSE' and requestedLabel != 'WORSE':
                worseTN += 1
            if goldLabel != 'NONE' and requestedLabel != 'NONE':
                noneTN += 1

            if goldLabel == 'BETTER' and requestedLabel != 'BETTER':
                betterFN += 1
            if goldLabel == 'WORSE' and requestedLabel != 'WORSE':
                worseFN += 1
            if goldLabel == 'NONE' and requestedLabel != 'NONE':
                noneFN += 1
            index += 1

        # with open('./csv/evaluated_with_t_' + str(treshold) + '.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(objectList2)

        print('with ' + str(treshold) + ' as treshold:')
        print('wrong: ' + str(totalWrong) + ' vs. right: ' + str(totalRight))
        print('In Total ' + str(totalRight*100 /
                                (totalRight+totalWrong)) + '% were right')

        betterDivide = betterTP + betterTN + betterFP + betterFN
        bAccuracy = '1'
        if betterDivide > 0:
            bAccuracy = str((betterTP + betterTN)/betterDivide)
        print('BETTER-Accuracy: ' + bAccuracy)

        worseDivide = worseTP + worseTN + worseFP + worseFN
        wAccuracy = '1'
        if worseDivide > 0:
            wAccuracy = str((worseTP + worseTN)/worseDivide)
        print('WORSE-Accuracy: ' + wAccuracy)

        noneDivide = noneTP + noneTN + worseFP + worseFN
        nAccuracy = '1'
        if noneDivide > 0:
            nAccuracy = str((noneTP + noneTN)/noneDivide)
        print('NONE-Accuracy: ' + nAccuracy)

        print('')


main()