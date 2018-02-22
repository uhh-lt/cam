import constants


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
    aPos = sentence.find(objA)  # position of objectA in sentence
    bPos = sentence.find(objB)  # position of objectB in sentence
    if aPos < bPos:
        # looks for a 'not' between A and B
        n = sentence.find('not', aPos, bPos)
    else:
        # looks for a 'not' between B and A
        n = sentence.find('not', bPos, aPos)
    for s in constants.BETTER_MARKERS:  # look for a betterMarker
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
    for s in constants.WORSE_MARKERS:  # look for a worseMarker
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
