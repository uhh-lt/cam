import constants
import aspect_searcher


def find_winner(sentences, objA, objB, aspects):
    '''

    '''
    for s in sentences:
        a_won = is_better_than(s, objA, objB)
        if a_won is not None:  # sentence is usable
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
    final_dict = {}
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
    final_dict['main aspects object 1'] = aspect_searcher.extract_main_aspects(objA.sentences, objA.name, objB.name)
    final_dict['main aspects object 2'] = aspect_searcher.extract_main_aspects(objB.sentences, objA.name, objB.name)
    final_dict['object a sentences'] = objA.sentences
    final_dict['object b sentences'] = objB.sentences
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
    n = sentence.find('not', first_pos, second_pos)
    for s in constants.POSITIVE_MARKERS:  # look for a betterMarker
        pos = sentence.find(s)
        if pos != -1 and pos > first_pos and pos < second_pos:  # found a betterMarker in sentence
            if first_pos == b_pos:  # betterMarker is between B and A
                if n != -1:  # a 'not' exists between the objects
                    return True
                else:
                    return False
            else:  # betterMarker is between A and B
                if n != -1:  # a 'not' exists between the objects
                    return False
                else:
                    return True
    for s in constants.POSITIVE_MARKERS:  # look for a worseMarker
        pos = sentence.find(s)
        if pos != -1:  # found a worseMarker in sentence
            if first_pos == b_pos:  # worseMarker is between B and A
                if n != -1:  # a 'not' exists between the objects
                    return False
                else:
                    return True
            else:  # worseMarker is between A and B
                if n != -1:  # a 'not' exists between the objects
                    return True
                else:
                    return False