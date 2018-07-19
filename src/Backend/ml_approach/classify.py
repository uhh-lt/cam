from pandas import DataFrame
from utils.answer_preparation import add_points, prepare_sentence_list, build_final_dict
from utils.regex_service import find_aspects
from heuristics.negation_dissolve_heuristic import negation_dissolve_heuristic

import re
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "cam_pretrained"))

from cam_pretrained.model_util import load_model


def classify_sentences(sentences, model):
    if model == 'infersent':
        model = load_model('data/model.pkl', glove_path='data/glove.840B.300d.txt',
                           infersent_path='data/infersent.allnli.pickle')
    else:
        model = load_model('data/bow_model.pkl',
                           glove_path=None, infersent_path=None)
    df = DataFrame(model.predict_proba(sentences), columns=model.classes_)
    df['max'] = df.idxmax(axis=1)
    return df


def evaluate(sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects):

    if sentences.values():
        max_sentscore = max(sentences.values())

    for index, row in prepared_sentences.iterrows():
        label = classification_results['max'][index]
        if label == 'NONE' or classification_results[label][index] < 0.66:
            continue

        classification_confidence = classification_results[label][index]
        sentence = row['sentence']
        contained_aspects = find_aspects(sentence, aspects)
        if (label == 'BETTER' and row['object_a'] == obj_a.name) or (label == 'WORSE' and row['object_b'] == obj_a.name):
            add_points(contained_aspects, obj_a,
                       sentences[sentence], sentence, max_sentscore, classification_confidence, score_function)
        else:
            add_points(contained_aspects, obj_b,
                       sentences[sentence], sentence, max_sentscore, classification_confidence, score_function)

    for aspect in aspects:
        negation_dissolve_heuristic(obj_a, obj_b, aspect.name)

    obj_a.sentences = prepare_sentence_list(obj_a.sentences)
    obj_b.sentences = prepare_sentence_list(obj_b.sentences)

    return build_final_dict(obj_a, obj_b)


def score_function(sentence_score, max_sentscore, weight, confidence):
    if weight < 1:
        weight = 1
    return (sentence_score + confidence * max_sentscore) * weight
