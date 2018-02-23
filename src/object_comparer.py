import constants
import aspect_searcher


def find_winner(sentences, objA, objB, aspects):
    '''

    '''
    for s in sentences:
        a_won = is_better_than(s, objA, objB)
        if a_won is not None:  # sentence is usable
            s_contains_aspect = aspect_searcher.find_aspect(s, aspects)
            if a_won:  # objectA won the sentence
                if s_contains_aspect:
                    objA.add_points(aspects[s_contains_aspect])
                else:
                    objA.add_points(1)
                objA.add_sentences(s)
            elif not a_won:  # objectB won the sentence
                if s_contains_aspect:
                    objB.add_points(aspects[s_contains_aspect])
                else:
                    objB.add_points(1)
                objB.add_sentences(s)
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
    aPos = sentence.find(objA.name)  # position of objectA in sentence
    bPos = sentence.find(objB.name)  # position of objectB in sentence
    if aPos < bPos:
        # looks for a 'not' between A and B
        n = sentence.find('not', aPos, bPos)
    else:
        # looks for a 'not' between B and A
        n = sentence.find('not', bPos, aPos)
    for s in constants.POSITIVE_MARKERS:  # look for a betterMarker
        pos = sentence.find(s)
        if pos != -1:  # found a betterMarker in sentence
            if (pos < aPos and pos > bPos):  # betterMarker is between B and A
                if n != -1:  # a 'not' exists between the objects
                    return True
                else:
                    return False
            elif (pos > aPos and pos < bPos):  # betterMarker is between A and B
                if n != -1:  # a 'not' exists between the objects
                    return False
                else:
                    return True
    for s in constants.POSITIVE_MARKERS:  # look for a worseMarker
        pos = sentence.find(s)
        if pos != -1:  # found a worseMarker in sentence
            if (pos < aPos and pos > bPos):  # worseMarker is between B and A
                if n != -1:  # a 'not' exists between the objects
                    return False
                else:
                    return True
            elif (pos > aPos and pos < bPos):  # worseMarker is between A and B
                if n != -1:  # a 'not' exists between the objects
                    return True
                else:
                    return False
    return None  # no better or worse marker was found between both objects