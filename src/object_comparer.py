import constants
import aspect_searcher
import marker_searcher


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
    for s in sentences:
        a_won = is_better_than(s, objA, objB)
        # the aspects the user entered that are contained in the sentence
        s_contains_aspects = aspect_searcher.find_aspects(s, aspects)
        if a_won:  # objectA won the sentence
            if s_contains_aspects:
                for aspect in s_contains_aspects:
                    objA.add_points(aspect.weight)
            else:
                objA.add_points(1)
            objA.add_sentence(s)
        elif not a_won:  # objectB won the sentence
            if s_contains_aspects:
                for aspect in s_contains_aspects:
                    objB.add_points(aspect.weight)
            else:
                objB.add_points(1)
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
    final_dict['main aspects object 1'] = aspect_searcher.extract_main_aspects(
        objA.sentences, objA.name, objB.name)
    final_dict['main aspects object 2'] = aspect_searcher.extract_main_aspects(
        objB.sentences, objA.name, objB.name)
    final_dict['object 1 sentences'] = objA.sentences
    final_dict['object 2 sentences'] = objB.sentences
    return final_dict


def is_better_than(sentence, objA, objB):
    '''
    Analyzes a sentence that contains two given objects. Returns True if the sentence
    suggests that objA is better than objB, False if it suggests the opposite and
    None if the sentence doesn't suggest a clear answer.
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
    a_pos = sentence.find(objA.name)  # position of objectA in sentence
    b_pos = sentence.find(objB.name)  # position of objectB in sentence
    first_pos = min(a_pos, b_pos)
    second_pos = max(a_pos, b_pos)
    opp_pos = marker_searcher.get_marker_pos(sentence, first_pos, second_pos, constants.OPPOSITE_MARKERS)
    positive_pos = marker_searcher.get_marker_pos(sentence, first_pos, second_pos, constants.POSITIVE_MARKERS)
    if positive_pos != -1: # there's a positive marker, check if a won
        return objA_wins_sentence(sentence, first_pos, second_pos, a_pos, b_pos, opp_pos, positive_pos)
        # we can return because there's never both markers in a sentence
    negative_pos = marker_searcher.get_marker_pos(sentence, first_pos, second_pos, constants.NEGATIVE_MARKERS)
    # we're only here if there's no positive marker, so there must be negative one
    return not objA_wins_sentence(sentence, first_pos, second_pos, a_pos, b_pos, opp_pos, negative_pos)

def objA_wins_sentence(sentence, first_pos, second_pos, a_pos, b_pos, opp_pos, marker_pos):
    if opp_pos != -1:
        if first_pos < opp_pos < marker_pos:
            return False if first_pos == a_pos else True # example: a is not better than b
    else:
        return True if first_pos == a_pos else False # example> a is better than b
        