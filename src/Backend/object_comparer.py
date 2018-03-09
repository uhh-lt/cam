from constants import OPPOSITE_MARKERS, POSITIVE_MARKERS, NEGATIVE_MARKERS, NEGATIONS
from aspect_searcher import find_aspects
from marker_searcher import get_marker_count, get_marker_pos
from link_extracter import extract_main_links
import re


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
    max_sentscore = 0
    for key in sentences:
        max_sentscore = max(max_sentscore, sentences[key])
    for s in sentences:
        comp_result = what_is_better(s, obj_a, obj_b)
        # the aspects the user entered that are contained in the sentence
        contained_aspects = find_aspects(s, aspects)
        if comp_result['winner'] == obj_a:  # objectA won the sentence
            if contained_aspects:
                for aspect in contained_aspects:
                    obj_a.add_points(
                        (sentences[s] / max_sentscore) * aspect.weight)
                    obj_a.add_points(
                        (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            else:
                # multiple markers, multiple points
                obj_a.add_points(
                    (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            obj_a.add_sentence(s)
        else:  # objectB won the sentence
            if contained_aspects:
                for aspect in contained_aspects:
                    obj_b.add_points(
                        (sentences[s] / max_sentscore) * aspect.weight)
                    obj_a.add_points(
                        (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            else:
                obj_b.add_points(
                    (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            obj_b.add_sentence(s)
    return build_final_dict(obj_a, obj_b)


def build_final_dict(obj_a, obj_b):
    '''
    Builds the final dictionary containing all necessary information regarding the comparison to 
    be returned to the frontend.

    obj_a:  Argument
            the first object of the comparison

    obj_b:  Argument
            the second object of the comparison
    '''
    final_dict = {}  # the dictionary to be returned
    if obj_a.points > obj_b.points:
        final_dict['winner'] = obj_a.name
    elif obj_b.points > obj_a.points:
        final_dict['winner'] = obj_b.name
    else:
        final_dict['winner'] = 'No winner found'
    final_dict['object 1'] = obj_a.name
    final_dict['object 2'] = obj_b.name
    final_dict['score object 1'] = obj_a.points
    final_dict['score object 2'] = obj_b.points
    linked_words = extract_main_links(
        obj_a.sentences, obj_b.sentences, obj_a, obj_b)
    final_dict['extracted aspects object 1'] = linked_words['A']
    final_dict['extracted aspects object 2'] = linked_words['B']
    final_dict['object 1 sentences'] = obj_a.sentences
    final_dict['object 2 sentences'] = obj_b.sentences
    return final_dict


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
    # position of objectA in sentence, spaces to not find objname as part of different word
    wordlist = re.compile('[A-Za-z]+').findall(sentence)
    a_pos = 0
    if obj_a.name in wordlist:
        a_pos = wordlist.index(obj_a.name)
    # position of objectB in sentence, spaces to not find objname as part of different word
    b_pos = 0
    if obj_b.name in wordlist:
        b_pos = wordlist.index(obj_b.name)
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
    if opp_pos != -1:
        if first_pos < opp_pos < marker_pos:
            return False if first_pos == a_pos else True  # example: a is not better than b
    elif neg_pos != -1:
        if first_pos < neg_pos < marker_pos:
            # example: a couldn't be better than b
            return False if first_pos == a_pos else True
    else:
        return True if first_pos == a_pos else False  # example: a is better than b
