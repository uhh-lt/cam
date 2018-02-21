'''
Contains a method for analyzing a sentence (comparing two objects).
'''

betterMarkers = ['better', 'easier', 'faster', 'nicer', 'wiser', 'cooler', 'decent', 'safer', 'superior', 'solid', 'terrific']
worseMarkers = ['worse', 'harder', 'slower', 'poorly', 'uglier', 'poorer', 'lousy', 'nastier', 'inferior', 'mediocre']

def analyze(sentence, objA, objB):
    '''
    Analyzes a sentence that contains two given objects. Returns objA, if the sentence
    suggests that objA is "better" than objB, objB if it suggests the opposite and
    False if the sentence doesn't suggest a clear answer.

    sentence:   String
                the sentence to analyze. Has to contain objA and objB.
    objA:       String
                the first object to be compared to the second.
    objB:       String
                the second object to be compared to the first.
    '''
    aPos = sentence.find(objA) #position of objectA in sentence
    bPos = sentence.find(objB) #position of objectB in sentence
    if aPos < bPos:
        n = sentence.find('not', aPos, bPos) #looks for a 'not' between A and B
    else:
        n = sentence.find('not', bPos, aPos) #looks for a 'not' between B and A
    for s in betterMarkers: #look for a betterMarker
        pos = sentence.find(s)
        if pos != -1: #found a betterMarker in sentence
            if (pos < aPos and pos > bPos): #betterMarker is between B and A
                if n != -1: #a 'not' exists between the objects
                    return objA
                else:
                    return objB
            elif (pos > aPos and pos < bPos): #betterMarker is between A and B
                if n != -1: #a 'not' exists between the objects
                    return objB
                else:
                    return objA
    for s in worseMarkers: #look for a worseMarker
        pos = sentence.find(s)
        if pos != -1: #found a worseMarker in sentence
            if (pos < aPos and pos > bPos): #worseMarker is between B and A
                if n != -1: #a 'not' exists between the objects
                    return objB
                else:
                    return objA
            elif (pos > aPos and pos < bPos): #worseMarker is between A and B
                if n != -1: #a 'not' exists between the objects
                    return objA
                else:
                    return objB
    return False #no better or worse marker was found between both objects