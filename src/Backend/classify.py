import aspect_searcher
import object_comparer
from pandas import DataFrame

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "cam_pretrained"))

from cam_pretrained.model_util import load_model

def classify_sentences(sentences, model):
    if model == 'infersent':
        model = load_model('data/model.pkl', glove_path='data/glove.840B.300d.txt', infersent_path='data/infersent.allnli.pickle')
    else:
        model = load_model('data/bow_model.pkl', glove_path=None, infersent_path=None)
    df = DataFrame(model.predict_proba(sentences), columns=model.classes_)
    df['max'] = df.idxmax(axis=1)
    return df


def evaluate(sentences, prepared_sentences, classification_results, obj_a, obj_b, aspects):

    if sentences.values():
        max_sentscore = max(sentences.values())

    for index, row in prepared_sentences.iterrows():
        label = classification_results['max'][index]
        if label == 'NONE':
            continue

        classification_confidence = classification_results[label][index]
        sentence = row['sentence']
        contained_aspects = aspect_searcher.find_aspects(sentence, aspects)
        if (label == 'BETTER' and row['object_a'] == obj_a.name) or (label == 'WORSE' and row['object_b'] == obj_a.name):
            add_points(contained_aspects, obj_a, sentences[sentence], sentence, max_sentscore, classification_confidence)
        else:
            add_points(contained_aspects, obj_b, sentences[sentence], sentence, max_sentscore, classification_confidence)
        
    obj_a.sentence_with_aspect = prepare_sentence_list(obj_a.sentence_with_aspect)
    obj_b.sentence_with_aspect = prepare_sentence_list(obj_b.sentence_with_aspect)
    obj_a.sentences = prepare_sentence_list(obj_a.sentences)
    obj_b.sentences = prepare_sentence_list(obj_b.sentences)

    return object_comparer.build_final_dict(obj_a, obj_b)

def prepare_sentence_list(sentences_with_confidence):
    sentences_with_confidence.sort(reverse = True)
    return list(DataFrame(sentences_with_confidence, columns=['confidence', 'sentence'])['sentence'])

def add_points(contained_aspects, winner, sentence_score, sentence, max_sentscore, classification_confidence):
    if contained_aspects:
        for aspect in contained_aspects:
            winner.add_points((sentence_score / max_sentscore) * aspect.weight * max_sentscore)
        winner.add_sentence_with_aspect([classification_confidence, sentence])
    else:
        winner.add_points(sentence_score / max_sentscore)
        winner.add_sentence([classification_confidence, sentence])
