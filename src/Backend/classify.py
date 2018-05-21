import pandas as pd
from sklearn.externals import joblib
import aspect_searcher
import object_comparer

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "cam_pretrained"))

from cam_pretrained.model_util import load_model


def classify_sentences(sentences):
    # model = load_model('data/bow_model.pkl', glove_path=None, infersent_path=None)
    model = load_model('data/bow_model_XGB.pkl', glove_path=None, infersent_path=None)
    # model = load_model('data/model_2.pkl', glove_path='data/glove.840B.300d.txt', infersent_path='data/infersent.allnli.pickle')
    return model.predict(sentences)


def evaluate(sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects):

    max_sentscore = max(sentences.values())

    for index, row in prepared_sentences.iterrows():
        label = classification_results[index]
        if label == 'NONE':
            continue

        sentence = row['sentence']
        contained_aspects = aspect_searcher.find_aspects(sentence, aspects)
        if (label == 'BETTER' and row['object_a'] == obj_a.name) or (label == 'WORSE' and row['object_b'] == obj_a.name):
            add_points(contained_aspects, obj_a, sentences[sentence], sentence, max_sentscore)
        else:
            add_points(contained_aspects, obj_b, sentences[sentence], sentence, max_sentscore)
    return object_comparer.build_final_dict(obj_a, obj_b)


def add_points(contained_aspects, winner, sentence_score, sentence, max_sentscore):
    if contained_aspects:
        for aspect in contained_aspects:
            winner.add_points((sentence_score / max_sentscore) * aspect.weight * max_sentscore)
        winner.add_sentence_with_aspect(sentence)
    else:
        winner.add_sentence(sentence)
        winner.add_points(sentence_score / max_sentscore)
