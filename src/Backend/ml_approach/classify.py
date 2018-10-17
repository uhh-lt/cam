from pandas import DataFrame
from utils.answer_preparation import add_points, prepare_sentence_list, build_final_dict
from utils.regex_service import find_aspects
from heuristics.negation_dissolve_heuristic import negation_dissolve_heuristic

import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "cam_pretrained"))

from cam_pretrained.model_util import load_model

USE_HEURISTICS = True


def classify_sentences(sentences, model):
    if model == 'infersent':
        model = load_model('data/infersent_model.pkl', glove_path='data/glove.840B.300d.txt',
                           infersent_path='data/infersent.allnli.pickle')
    else:
        model = load_model('data/bow_model.pkl',
                           glove_path=None, infersent_path=None)
    df = DataFrame(model.predict_proba(sentences), columns=model.classes_)
    df['max'] = df.idxmax(axis=1)
    return df


def count_confindences(prepared_sentences, classification_results, aspects):
    perfect = 0
    excellent = 0
    good = 0
    medium = 0
    ok = 0

    for index, row in prepared_sentences.iterrows():
        if len(find_aspects(row['sentence'], aspects)) == 0:
            continue
        label = classification_results['max'][index]
        if label != 'NONE':
            confidence = classification_results[label][index]
            if confidence > 0.8:
                perfect += 1
            elif confidence > 0.7:
                excellent += 1
            elif confidence > 0.6:
                good += 1
            elif confidence > 0.5:
                medium += 1
            else:
                ok += 1

    excellent += perfect
    good += excellent
    medium += good
    ok += medium

    return (excellent, good, medium, ok)


def find_threshold(counted_confidences, sentence_threshold):

    threshold = 0
    if counted_confidences[0] > sentence_threshold:
        threshold = 0.8
    elif counted_confidences[1] > sentence_threshold:
        threshold = 0.7
    elif counted_confidences[2] > sentence_threshold:
        threshold = 0.6
    elif counted_confidences[3] > sentence_threshold:
        threshold = 0.5

    print('Uses threshold', threshold)
    return threshold


def evaluate(sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects):

    if len(sentences) > 0:
        max_sentscore = max(sentence.ES_score for sentence in sentences)

    counts = count_confindences(
        prepared_sentences, classification_results, aspects)
    threshold_sentences = find_threshold(counts, 5)
    threshold_score = find_threshold(counts, 3)

    for index, row in prepared_sentences.iterrows():
        label = classification_results['max'][index]
        if label == 'NONE':
            continue

        classification_confidence = classification_results[label][index]
        sentence_text = row['sentence']

        for s in sentences:
            if s.text == sentence_text:
                sentence = s
                break
        sentences.remove(sentence)
        sentence.set_confidence(classification_confidence.item())
        
        contained_aspects = find_aspects(sentence.text, aspects)
        if (label == 'BETTER' and row['object_a'] == obj_a.name) or (label == 'WORSE' and row['object_b'] == obj_a.name):
            add_points(contained_aspects, obj_a, sentence,
                       max_sentscore, score_function, threshold_sentences, threshold_score)
        else:
            add_points(contained_aspects, obj_b, sentence,
                       max_sentscore, score_function, threshold_sentences, threshold_score)

    if USE_HEURISTICS:
        for aspect in aspects:
            negation_dissolve_heuristic(obj_a, obj_b, aspect.name, aspects, threshold_score)
            negation_dissolve_heuristic(obj_b, obj_a, aspect.name, aspects, threshold_score)

    obj_a.sentences = prepare_sentence_list(obj_a.sentences)
    obj_b.sentences = prepare_sentence_list(obj_b.sentences)

    return build_final_dict(obj_a, obj_b, sentences)


def score_function(sentence, max_sentscore, weight, threshold):
    if weight < 1:
        weight = 1
    # return (sentence_score + confidence * max_sentscore) * weight

    score = 0
    if sentence.confidence > threshold:
        score += max_sentscore

    return score + sentence.ES_score + max_sentscore * weight
    # return sentence_score * weight
    # return confidence * weight


def set_use_heuristics(use_heuristics):
    global USE_HEURISTICS
    USE_HEURISTICS = use_heuristics
