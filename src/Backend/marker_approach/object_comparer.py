from marker_approach.constants import OPPOSITE_MARKERS, POSITIVE_MARKERS, NEGATIVE_MARKERS, NEGATIONS
from marker_approach.marker_searcher import get_marker_count, get_marker_pos

from utils.regex_service import find_aspects, find_pos_in_sentence
from utils.answer_preparation import add_points, prepare_sentence_list, build_final_dict



def find_winner(sentences, obj_a, obj_b, aspects):
    '''
    Finds the winner of two objects for given sentences and aspects. Returns a dictionary
    containing all the information of the comparison (winner, sentences for each object, score for
    each object and more).

    sentences:  Dictionary
                dictionary containing sentences

    obj_a:      Argument
                the first competing object

    obj_b:      Argument
                the second competing object

    aspects:    List
                list of Aspects
    '''
    if len(sentences) > 0:
        max_sentscore = max(sentence.ES_score for sentence in sentences)
    for sentence in sentences:
        comp_result = what_is_better(sentence.text, obj_a, obj_b)
        sentence.set_confidence(comp_result['marker_cnt'])
        if comp_result['winner'] == obj_a:  # objectA won the sentence
            add_points(find_aspects(sentence.text, aspects), obj_a,
                       sentence, max_sentscore, score_function)
        else:  # objectB won the sentence
            add_points(find_aspects(sentence.text, aspects), obj_b,
                       sentence, max_sentscore, score_function)

    obj_a.sentences = prepare_sentence_list(obj_a.sentences)
    obj_b.sentences = prepare_sentence_list(obj_b.sentences)

    return build_final_dict(obj_a, obj_b, sentences)




def score_function(sentence, max_sentscore, weight, threshold):
    return (sentence.ES_score / max_sentscore) * (weight + sentence.confidence)



def what_is_better(sentence, obj_a, obj_b):
    '''
    Analyzes a sentence that contains two given objects. Returns object containing winner
    and a boolean marking multiple markers.
    Currently only sentences are supported that are built in the form of
        ... object ... marker ... object ...

    sentence:   String
                the sentence to analyze. Has to contain obj_a and obj_b.
    obj_a:      Argument
                the first object to be compared to the second.
    obj_b:      Argument
                the second object to be compared to the first.
    '''
    sentence = sentence.lower()
    result = {}

    a_pos = find_pos_in_sentence(obj_a.name, sentence)
    b_pos = find_pos_in_sentence(obj_b.name, sentence)

    first_pos = min(a_pos, b_pos)
    second_pos = max(a_pos, b_pos)
    opp_pos = get_marker_pos(sentence, first_pos, second_pos, OPPOSITE_MARKERS)
    neg_pos = get_marker_pos(sentence, first_pos, second_pos, NEGATIONS)
    positive_pos = get_marker_pos(
        sentence, first_pos, second_pos, POSITIVE_MARKERS)
    if positive_pos != -1:  # there's a positive marker, check if a won
        result['marker_cnt'] = get_marker_count(
            sentence, first_pos, second_pos, POSITIVE_MARKERS)
        result['winner'] = obj_a if obj_a_wins_sentence(
            first_pos, a_pos, opp_pos, neg_pos, positive_pos) else obj_b
        return result
        # we can return because there's never both markers in a sentence
    negative_pos = get_marker_pos(
        sentence, first_pos, second_pos, NEGATIVE_MARKERS)
    result['marker_cnt'] = get_marker_count(
        sentence, first_pos, second_pos, NEGATIVE_MARKERS)
    # we're only here if there's no positive marker, so there must be negative one
    result['winner'] = obj_b if obj_a_wins_sentence(
        first_pos, a_pos, opp_pos, neg_pos, negative_pos) else obj_a
    return result


def obj_a_wins_sentence(first_pos, a_pos, opp_pos, neg_pos, marker_pos):
    '''
    Returns whether obj_a wins the sentence or not.

    first_pos:  number
                the first position of one of the objects within the sentence

    a_pos:      number
                the position of obj_a within the sentence

    opp_pos:    number
                the position of an opposite marker within the sentence

    neg_pos:    number
                the position of a negation within the sentence

    marker_pos: number
                the position of a marker within the sentence
    '''
    if opp_pos != -1 and first_pos < opp_pos < marker_pos:
        return first_pos != a_pos  # example: a is not better than b
    elif neg_pos != -1 and first_pos < neg_pos < marker_pos:
        return first_pos != a_pos  # example: a couldn't be better than b
    else:
        return first_pos == a_pos  # example: a is better than b
