import constants
import aspect_searcher


def find_winner(sentences, objA, objB, aspects):
    '''

    '''
    aPoints = 0  # counts how many times objA won a sentence.
    bPoints = 0  # counts how many times objB won a sentence.
    aSentences = []  # collects all sentences objA has won.
    bSentences = []  # collects all sentences objB has won.
    for s in sentences:
        a_won = is_better_than(s, objA, objB)
        if a_won is not None:  # sentence is usable
            s_contains_aspect = aspect_searcher.find_aspect(s, aspects)
            if a_won:  # objectA won the sentence
                if s_contains_aspect:
                    aPoints += aspects[s_contains_aspect]
                else:
                    aPoints += 1
                aSentences.append(s)
            elif not a_won:  # objectB won the sentence
                if s_contains_aspect:
                    aPoints += aspects[s_contains_aspect]
                else:
                    bPoints += 1
                bSentences.append(s)
    final_dict = {}
    if aPoints > bPoints:
        final_dict['winner'] = objA
    elif bPoints > aPoints:
        final_dict['winner'] = objB
    else:
        final_dict['winner'] = None
    final_dict['object 1'] = objA
    final_dict['object 2'] = objB
    final_dict['score object 1'] = aPoints
    final_dict['score object 2'] = bPoints
    final_dict['main aspects object 1'] = aspect_searcher.extract_main_aspects(aSentences, objA, objB)
    final_dict['main aspects object 2'] = aspect_searcher.extract_main_aspects(bSentences, objA, objB)
    final_dict['object a sentences'] = aSentences
    final_dict['object b sentences'] = bSentences
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
    aPos = sentence.find(objA)  # position of objectA in sentence
    bPos = sentence.find(objB)  # position of objectB in sentence
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