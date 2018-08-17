def set_counts(score, gold_score, deviation, score_counts):
    none_range = 0.1
    worse_start = (1 - none_range) / 2
    better_start = 1 - worse_start

    # Set true-positives
    if deviation < worse_start and gold_score in [1, 0] or deviation < (none_range / 2) and gold_score == 0.5:
        score_counts.totalRight += 1
        if score > better_start:
            score_counts.betterTP += 1
        elif score < worse_start:
            score_counts.worseTP += 1
        else:
            score_counts.noneTP += 1
    else:  # Set false-positives
        score_counts.totalWrong += 1
        if score > better_start:
            score_counts.betterFP += 1
        elif score < worse_start:
            score_counts.worseFP += 1
        else:
            score_counts.noneFP += 1

    # Set the true-negatives
    if gold_score < 1 and score < better_start:
        score_counts.betterTN += 1
    if gold_score > 0 and score > worse_start:
        score_counts.worseTN += 1
    if gold_score != 0.5 and (score > better_start or score < worse_start):
        score_counts.noneTN += 1

    # Set the false-negative
    if gold_score == 1 and score < better_start:
        score_counts.betterFN += 1
    if gold_score == 0 and score > worse_start:
        score_counts.worseFN += 1
    if gold_score == 0.5 and (score > better_start or score < worse_start):
        score_counts.noneFN += 1


def calculateEvaluationScores(label, TP, TN, FP, FN, digits, totalAcc):

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

    return [label, precision, recall, f1, accuracy, totalAcc]

class Scores:
    def __init__(self):
        self.totalRight = 0
        self.totalWrong = 0
        self.betterTP = 0
        self.betterFP = 0
        self.betterTN = 0
        self.betterFN = 0
        self.worseTP = 0
        self.worseFP = 0
        self.worseTN = 0
        self.worseFN = 0
        self.noneTP = 0
        self.noneFP = 0
        self.noneTN = 0
        self.noneFN = 0