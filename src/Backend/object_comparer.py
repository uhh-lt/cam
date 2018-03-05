import constants
import aspect_searcher
import marker_searcher
import link_extracter


def find_winner(sentences, objA, objB, aspects):
    '''
    Finds the winner of two objects for a given list of sentences and aspects.

    sentences:  List
                list of sentences

    objA:       Argument
                the first competing object

    objB:       Argument
                the second competing object

    aspects:    List
                list of Aspects
    '''
    max_sentscore = 0
    for key in sentences:
        max_sentscore = max(max_sentscore, sentences[key])
    for s in sentences:
        comp_result = what_is_better(s, objA, objB)
        # the aspects the user entered that are contained in the sentence
        contained_aspects = aspect_searcher.find_aspects(s, aspects)
        if comp_result['winner'] == objA:  # objectA won the sentence
            if contained_aspects:
                for aspect in contained_aspects:
                    objA.add_points(
                        (sentences[s] / max_sentscore) * aspect.weight)
                    objA.add_points(
                        (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            else:
                # multiple markers, multiple points
                objA.add_points(
                    (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            objA.add_sentence(s)
        else:  # objectB won the sentence
            if contained_aspects:
                for aspect in contained_aspects:
                    objB.add_points(
                        (sentences[s] / max_sentscore) * aspect.weight)
                    objA.add_points(
                        (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            else:
                objB.add_points(
                    (sentences[s] / max_sentscore) * comp_result['marker_cnt'])
            objB.add_sentence(s)
    final_dict = {}  # the dictionary to be returned
    if objA.points > objB.points:
        final_dict['winner'] = objA.name
    elif objB.points > objA.points:
        final_dict['winner'] = objB.name
    else:
        final_dict['winner'] = None
    final_dict['object 1'] = objA.name
    final_dict['object 2'] = objB.name
    final_dict['score object 1'] = objA.points
    final_dict['score object 2'] = objB.points
    final_dict['main links object 1'] = link_extracter.extract_main_links(
        objA.sentences, objB.sentences, objA.name, objB.name)['A']
    final_dict['main links object 2'] = link_extracter.extract_main_links(
        objA.sentences, objB.sentences, objA.name, objB.name)['B']
    final_dict['main links both'] = link_extracter.extract_main_links(
        objA.sentences, objB.sentences, objA.name, objB.name)['both']
    final_dict['object 1 sentences'] = objA.sentences
    final_dict['object 2 sentences'] = objB.sentences
    return final_dict


def what_is_better(sentence, objA, objB):
    '''
    Analyzes a sentence that contains two given objects. Returns object containing winner
    and a boolean marking multiple markers.
    Currently only sentences are supported that are built in the form of
        ... object ... marker ... object ...

    sentence:   String
                the sentence to is_better_than. Has to contain objA and objB.
    objA:       String
                the first object to be compared to the second.
    objB:       String
                the second object to be compared to the first.
    '''
    sentence = sentence.lower()
    ''' TODO this is called also in sentence_clearer.remove_wrong_structure -> should refactor '''
    result = {}
    # position of objectA in sentence, spaces to not find objname as part of different word
    a_pos = sentence.find(objA.name)
    # position of objectB in sentence, spaces to not find objname as part of different word
    b_pos = sentence.find(objB.name)
    first_pos = min(a_pos, b_pos)
    second_pos = max(a_pos, b_pos)
    opp_pos = marker_searcher.get_marker_pos(
        sentence, first_pos, second_pos, constants.OPPOSITE_MARKERS)
    neg_pos = marker_searcher.get_marker_pos(
        sentence, first_pos, second_pos, constants.NEGATIONS)
    positive_pos = marker_searcher.get_marker_pos(
        sentence, first_pos, second_pos, constants.POSITIVE_MARKERS)
    if positive_pos != -1:  # there's a positive marker, check if a won
        result['marker_cnt'] = marker_searcher.get_marker_count(
            sentence, first_pos, second_pos, constants.POSITIVE_MARKERS)
        result['winner'] = objA if objA_wins_sentence(
            first_pos, a_pos, opp_pos, neg_pos, positive_pos) else objB
        return result
        # we can return because there's never both markers in a sentence
    negative_pos = marker_searcher.get_marker_pos(
        sentence, first_pos, second_pos, constants.NEGATIVE_MARKERS)
    result['marker_cnt'] = marker_searcher.get_marker_count(
        sentence, first_pos, second_pos, constants.NEGATIVE_MARKERS)
    # we're only here if there's no positive marker, so there must be negative one
    result['winner'] = objB if objA_wins_sentence(
        first_pos, a_pos, opp_pos, neg_pos, negative_pos) else objA
    return result


def objA_wins_sentence(first_pos, a_pos, opp_pos, neg_pos, marker_pos):
    if opp_pos != -1:
        if first_pos < opp_pos < marker_pos:
            return False if first_pos == a_pos else True  # example: a is not better than b
    elif neg_pos != -1:
        if first_pos < neg_pos < marker_pos:
            # example: a couldn't be better than b
            return False if first_pos == a_pos else True
    else:
        return True if first_pos == a_pos else False  # example: a is better than b
