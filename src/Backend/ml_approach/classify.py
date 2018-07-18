from pandas import DataFrame
from utils.answer_preparation import add_points, prepare_sentence_list, build_final_dict
from utils.regex_service import find_aspects
from utils.summarization import get_tag
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
    return ((sentence_score * confidence) / max_sentscore) * weight


contrary_comparatives = {
    'more': 'less',
    'bigger': 'smaller'
}
permissible_pattern = ['a_c_b', 'b_c_a']


def negation_dissolve_heuristic(object_a, object_b, aspect):
    print(object_a.name, object_b.name, aspect)

    tag_sentences_a = tag_sentences(
        object_a.sentences, object_a.name, object_b.name, aspect)
    tag_sentences_b = tag_sentences(
        object_b.sentences, object_a.name, object_b.name, aspect)

    if len(tag_sentences_a) == 0 or len(tag_sentences_b) == 0:
        return
    a_max_tag = max(tag_sentences_a.items(), key=lambda elem: len(elem[1]))[0]
    b_max_tag = max(tag_sentences_b.items(), key=lambda elem: len(elem[1]))[0]
    print(len(tag_sentences_a[a_max_tag]), len(tag_sentences_b[b_max_tag]))

    if a_max_tag in permissible_pattern or b_max_tag in permissible_pattern:
        if len(tag_sentences_a[a_max_tag]) > len(tag_sentences_b[b_max_tag]):
            print('A:', a_max_tag)
            move_assignment(a_max_tag, tag_sentences_b,
                            object_b, object_a, aspect)
        else:
            print('B:', b_max_tag)
            move_assignment(b_max_tag, tag_sentences_a,
                            object_a, object_b, aspect)


def move_assignment(from_max_tag, to_tag_sentences, from_object, to_object, aspect):
    turned_tag = turn_tag(from_max_tag)
    if turned_tag in to_tag_sentences:
        sentences_to_move = to_tag_sentences[turned_tag]
        points_to_move = 0
        print('For', '\'' + aspect + '\'', 'there were moved', len(sentences_to_move),
              'sentences from', from_object.name, 'to', to_object.name, '.')
        print('----')
        for sentence in sentences_to_move:
            print('-' + re.sub(' +', ' ',
                               re.sub('[^a-zA-Z0-9 ]', ' ', sentence[1])))
            points_to_move = points_to_move + sentence[0]
        print('----')
        from_object.sentences = [
            sentence for sentence in from_object.sentences if sentence not in sentences_to_move]
        from_object.points[aspect] = from_object.points[aspect] - \
            points_to_move
        from_object.totalPoints = from_object.totalPoints - points_to_move

        to_object.sentences.extend(sentences_to_move)
        to_object.points[aspect] = to_object.points[aspect] + points_to_move
        to_object.totalPoints = to_object.totalPoints + points_to_move

        print((points_to_move / (to_object.totalPoints +
                                 from_object.totalPoints)) * 100, '% moved (total)')
        print((points_to_move / (to_object.points[aspect] +
                                 from_object.points[aspect])) * 100, '% moved for', aspect)
    else:
        print('No sentences were moved.')


def tag_sentences(sentences, a_name, b_name, aspect):
    tag_sentences = {}
    for sentence in sentences:
        tag = get_tag(sentence[1], a_name, b_name, aspect)
        if tag == 'none':
            continue
        if tag in tag_sentences:
            tag_sentences[tag].append(sentence)
        else:
            tag_sentences[tag] = [sentence]
    return tag_sentences


def turn_tag(tag):
    return tag[-1:] + tag[1:-1] + tag[:1]
