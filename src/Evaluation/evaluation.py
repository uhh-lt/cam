import csv


def calculateLabel(winnerTreshold, scoreA, scoreB):
    '''
    Calculates the score by the given scores of the compared objects with respect to
    the given threshold. The threshold determines how much higher the score of one
    object must be to get selected as winner.

    @param winnerThreshold: in range from 0 > t >= 1, one object score must be at least
    1+(1-t) times bigger then the other to get selectd as winner

    @param scoreA: score of object a

    @param scoreB score of object b

    @returns the label according to the scores and to the threshold
    '''
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
    '''
    Load all lines of the csv file with the calculated scores and the gold label
    of the compared pairs and remove the header.

    @returns the content of the file as list
    '''
    listCSV = []
    with open(fileName, newline='', encoding='utf-8') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvReader:
            listCSV.append(row)
    listCSV.pop(0)
    return listCSV


def calculateEvaluationScores(TP, TN, FP, FN, digits, prefilledResult, totalAcc):
    '''
    Calculates precision, recall, accuracy and f1 score for the given parameters.

    @param TP: true positives

    @param TN: true negatives
    
    @param FP: false positives
    
    @param FN: false negatives
    
    @param digits: how many digits after the coma

    @param prefilledResult: contains the threshold and the label ob the tp, tn ...

    @totalAcc: empty string or for none its the total accuracy computed with the given
    threshold.

    @returns the prefilledResult filled with precison, recall etc.
    '''
    total = TP + TN + FP + FN
    accuracy = '1.0'
    if total > 0:
        accuracy = round((TP + TN) / total, digits)
    precision = round(TP / (TP + FP),
                      digits) if TP + FP > 0 else 1.0
    recall = round(TP / (TP + FN),
                   digits) if TP + FP > 0 else 1.0
    f1 = round(2 * (precision * recall) / (precision + recall),
               digits) if precision + recall > 0 else 0.0

    prefilledResult.extend([precision, recall, f1, accuracy, totalAcc])
    return prefilledResult


def main():
    '''
    Calculates the TP, TN, FN and FP for all labels, calculates Precision, Recall, F1 and accuracy
    and outputs it in a csv file.
    '''
    print('Start evaluating:')
    urlParam = 'related'
    requestedLabels = loadFromCSV(
        './csv/({})_requested_labels.csv'.format(urlParam))
    objectList2 = [['object_a', 'object_b', 'requested_label', 'gold_label']]

    PrReF1 = [['threshold', 'label', 'precision',
               'recall', 'f_1', 'accuracy', 'total accuracy']]

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

        PrReF1.append(calculateEvaluationScores(
            betterTP, betterTN, betterFP, betterFN, digits, [treshold, 'better'], ''))
        PrReF1.append(calculateEvaluationScores(
            worseTP, worseTN, worseFP, worseFN, digits, [treshold, 'worse'], ''))
        PrReF1.append(calculateEvaluationScores(
            noneTP, noneTN, noneFP, noneFN, digits, [treshold, 'none'], totalPercentRight))

        PrReF1.append(['', '', '', '', '', '', ''])

    with open('./csv/({})_prReF1.csv'.format(urlParam), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(PrReF1)


main()
