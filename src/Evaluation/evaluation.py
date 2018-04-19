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
    urlParam = '-'
    requestedLabels = loadFromCSV('./csv/({})_requested_labels.csv'.format(urlParam))
    objectList2 = [['object_a', 'object_b', 'requested_label', 'gold_label']]
    evaluation = [['treshold', 'wrong', 'right', 'total_percent_right',
                   'better_accuracy', 'worse_accuracy', 'none_accuracy']]
    PrReF1 = [['treshold', 'label', 'precision', 'recall', 'f_1', 'accuracy', 'total accuracy']]

    digits = 2

    for i in range(1, 11, 1):
        treshold = round(0.1*i, 1)
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

        for pair in requestedLabels:
            goldLabel = pair[3]
            requestedLabel = calculateLabel(
                treshold, float(pair[4]), float(pair[5]))
            objectList2.append([pair[1], pair[2], requestedLabel, goldLabel])

            # Set true-positives
            if requestedLabel == goldLabel:
                totalRight += 1
                if requestedLabel == 'BETTER':
                    betterTP += 1
                elif requestedLabel == 'WORSE':
                    worseTP += 1
                else:
                    noneTP += 1
            else:  # Set false-positives
                totalWrong += 1
                if requestedLabel == 'BETTER':
                    betterFP += 1
                elif requestedLabel == 'WORSE':
                    worseFP += 1
                else:
                    noneFP += 1

            # Set the true-negatives
            if goldLabel != 'BETTER' and requestedLabel != 'BETTER':
                betterTN += 1
            if goldLabel != 'WORSE' and requestedLabel != 'WORSE':
                worseTN += 1
            if goldLabel != 'NONE' and requestedLabel != 'NONE':
                noneTN += 1

            # Set the false-negative
            if goldLabel == 'BETTER' and requestedLabel != 'BETTER':
                betterFN += 1
            if goldLabel == 'WORSE' and requestedLabel != 'WORSE':
                worseFN += 1
            if goldLabel == 'NONE' and requestedLabel != 'NONE':
                noneFN += 1

        totalPercentRight = round(
            totalRight * 100 / (totalRight + totalWrong), 2)

        betterDivide = betterTP + betterTN + betterFP + betterFN
        bAccuracy = '1.0'
        if betterDivide > 0:
            bAccuracy = round((betterTP + betterTN) / betterDivide, digits)
        bPrecision = round(betterTP / (betterTP + betterFP),
                           digits) if betterTP + betterFP > 0 else 1.0
        bRecall = round(betterTP / (betterTP + betterFN),
                        digits) if betterTP + betterFP > 0 else 1.0
        bF1 = round(2 * (bPrecision * bRecall) / (bPrecision + bRecall),
                    digits) if bPrecision + bRecall > 0 else 0.0

        PrReF1.append([treshold, 'better', bPrecision,
                       bRecall, bF1, bAccuracy, ''])

        worseDivide = worseTP + worseTN + worseFP + worseFN
        wAccuracy = '1.0'
        if worseDivide > 0:
            wAccuracy = round((worseTP + worseTN) / worseDivide, digits)
        wPrecision = round(worseTP / (worseTP + worseFP),
                           digits) if worseTP + worseFP > 0 else 1.0
        wRecall = round(worseTP / (worseTP + worseFN),
                        digits) if worseTP + worseFP > 0 else 1.0
        wF1 = round(2 * (wPrecision * wRecall) / (wPrecision + wRecall),
                    digits) if wPrecision + wRecall > 0 else 0.0

        PrReF1.append([treshold, 'worse', wPrecision,
                       wRecall, wF1, wAccuracy, ''])

        noneDivide = noneTP + noneTN + noneFP + noneFN
        nAccuracy = '1.0'
        if noneDivide > 0:
            nAccuracy = round((noneTP + noneTN) / noneDivide, digits)
        nPrecision = round(noneTP / (noneTP + noneFP),
                           digits) if noneTP + noneFP > 0 else 1.0
        nRecall = round(noneTP / (noneTP + noneFN),
                        digits) if noneTP + noneFP > 0 else 1.0
        nF1 = round(2 * (nPrecision * nRecall) / (nPrecision + nRecall),
                    digits) if nPrecision + nRecall > 0 else 0.0

        PrReF1.append([treshold, 'none', nPrecision, nRecall,
                       nF1, nAccuracy, totalPercentRight])

        # PrReF1.append(['', '', '', '', '', '', ''])

        evaluation.append([treshold, totalWrong, totalRight,
                           totalPercentRight, bAccuracy, wAccuracy, nAccuracy])

        print('with ' + str(treshold) + ' as treshold:')
        print('wrong: ' + str(totalWrong) + ' vs. right: ' + str(totalRight))
        print('In Total ' + str(totalPercentRight) + '% were right')
        print('BETTER-Accuracy: ' + str(bAccuracy))
        print('WORSE-Accuracy: ' + str(wAccuracy))
        print('NONE-Accuracy: ' + str(nAccuracy))
        print('')

    with open('./csv/({})_evaluation.csv'.format(urlParam), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(evaluation)

    with open('./csv/({})_prReF1.csv'.format(urlParam), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(PrReF1)


main()
