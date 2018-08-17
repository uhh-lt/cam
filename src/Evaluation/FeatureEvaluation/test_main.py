import csv
import sys
sys.path.append('../../Backend')
from utils.es_requester import request_es, extract_sentences, request_es_ML, request_es_triple
from utils.sentence_clearer import clear_sentences, remove_questions
from ml_approach.sentence_preparation_ML import prepare_sentence_DF
from ml_approach.classify import classify_sentences, evaluate
from marker_approach.object_comparer import find_winner
from main import Argument, Aspect

from score_determination import calculateEvaluationScores, set_counts, Scores
from evaluation_triples import triples


def simulate_main(triple):
    fast_search = 'true'
    obj_a = Argument(triple[1].lower().strip())
    obj_b = Argument(triple[2].lower().strip())
    aspects = [Aspect(triple[3].lower(), 5)]
    model = 'bow'
    # model = 'infersent'

    if aspects:
        json_compl_triples = request_es_triple(obj_a, obj_b, aspects)
    json_compl = request_es_ML(fast_search, obj_a, obj_b)

    if aspects:
        all_sentences = extract_sentences(json_compl_triples)
        all_sentences.update(extract_sentences(json_compl))
    else:
        all_sentences = extract_sentences(json_compl)

    remove_questions(all_sentences)

    prepared_sentences = prepare_sentence_DF(all_sentences, obj_a, obj_b)

    classification_results = classify_sentences(prepared_sentences, model)

    final_dict = evaluate(all_sentences, prepared_sentences,
                          classification_results, obj_a, obj_b, aspects)

    a_aspect_score = 0
    if triple[3] in final_dict['scoreObject1']:
        a_aspect_score = final_dict['scoreObject1'][triple[3]]
    b_aspect_score = 0
    if triple[3] in final_dict['scoreObject2']:
        b_aspect_score = final_dict['scoreObject2'][triple[3]]
    
    return [a_aspect_score, b_aspect_score]


def main():
    scores = [['index', 'a_score', 'b_score', 'gold_deviation']]
    score_counts = Scores()
    for triple in triples:

        temp_scores = simulate_main(triple)
        a_aspect_score = temp_scores[0]
        b_aspect_score = temp_scores[1]

        total_aspect_score = a_aspect_score + b_aspect_score

        if total_aspect_score == 0:
            print(triple[0], '---', 'Nothing found for: ', triple[0],
                  triple[1], triple[2], triple[3])
            scores.append([triple[0], 0, 0, ''])
        else:
            gold = triple[4]
            a_percent = (a_aspect_score / total_aspect_score)
            b_percent = (b_aspect_score / total_aspect_score)
            print(triple[0], '---', triple[1] + ':', a_percent, triple[2] + ':', b_percent, triple[3])
            deviation = a_percent - gold if a_percent > gold else gold - a_percent
            set_counts((a_aspect_score / total_aspect_score), gold, deviation, score_counts)

            scores.append([triple[0], a_percent, b_percent, deviation])

    summed_deviation = 0
    total = len(scores)
    for score in scores:
        if score[3] == '' or score[0] == 'index':
            total = total - 1
            continue
        summed_deviation = summed_deviation + float(score[3])

    print('Average deviation:', summed_deviation / total, 'Incorrect:', score_counts.totalWrong, 'Correct:', score_counts.totalRight)
    totalPercentRight = round(score_counts.totalRight * 100 / (score_counts.totalRight + score_counts.totalWrong), 2)
    evaluation_scores = [['label', 'precision', 'recall', 'f_1', 'accuracy', 'total accuracy']]
    evaluation_scores.append(calculateEvaluationScores('BETTER', score_counts.betterTP, score_counts.betterTN, score_counts.betterFP, score_counts.betterFN, 2, ''))
    evaluation_scores.append(calculateEvaluationScores('WORSE', score_counts.worseTP, score_counts.worseTN, score_counts.worseFP, score_counts.worseFN, 2, ''))
    evaluation_scores.append(calculateEvaluationScores('NONE', score_counts.noneTP, score_counts.noneTN, score_counts.noneFP, score_counts.noneFN, 2, totalPercentRight))
    with open('./eval_scores.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows([list(x) for x in zip(*evaluation_scores)])

    scores.append(['', '', 'ava. deviation:', summed_deviation/total])
    scores.append(['', '', 'Incorrect:', score_counts.totalWrong])

    with open('./aspect_scores.csv', 'w', newline='', encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerows(scores)


if __name__ == "__main__":
    main()
