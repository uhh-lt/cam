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


def evaluate(sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects):

    if len(sentences) > 0:
        max_sentscore = max(sentence.score for sentence in sentences)

    for index, row in prepared_sentences.iterrows():
        label = classification_results['max'][index]
        if label == 'NONE' or classification_results[label][index] < 0.6:
            continue

        classification_confidence = classification_results[label][index]
        sentence_text = row['sentence']

        for s in sentences:
            if s.text == sentence_text:
                sentence = s
                break
        sentences.remove(sentence)
        
        contained_aspects = find_aspects(sentence.text, aspects)
        if (label == 'BETTER' and row['object_a'] == obj_a.name) or (label == 'WORSE' and row['object_b'] == obj_a.name):
            add_points(contained_aspects, obj_a, sentence,
                       max_sentscore, classification_confidence, score_function)
        else:
            add_points(contained_aspects, obj_b, sentence,
                       max_sentscore, classification_confidence, score_function)

    if USE_HEURISTICS:
        for aspect in aspects:
            negation_dissolve_heuristic(obj_a, obj_b, aspect.name, aspects)
            negation_dissolve_heuristic(obj_b, obj_a, aspect.name, aspects)
        
        

    obj_a.sentences = prepare_sentence_list(obj_a.sentences)
    obj_b.sentences = prepare_sentence_list(obj_b.sentences)

    return build_final_dict(obj_a, obj_b, sentences)


def score_function(sentence_score, max_sentscore, weight, confidence):
    if weight < 1:
        weight = 1
    return (sentence_score + confidence * max_sentscore) * weight


def set_use_heuristics(use_heuristics):
    global USE_HEURISTICS
    USE_HEURISTICS=use_heuristics
