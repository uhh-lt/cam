import constants


def clear_sentences(sentences, objA, objB):
    '''
    Removes sentences which (currently) cannot be properly analyzed from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    sentences = remove_questions(sentences)
    sentences = remove_negations(sentences)
    sentences = remove_wrong_marker_positions(sentences, objA, objB)
    return sentences


def remove_questions(sentences):
    '''
    Removes questions from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    for s in sentences:
        if '?' in s:
            sentences.remove(s)
    return sentences


def remove_negations(sentences):
    '''
    Removes negations from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    for s in sentences:
        for neg in constants.NEGATIONS:
            if neg in s:
                sentences.remove(s)
                break
    return sentences
'''
def remove_double_markers(sentences, objA, objB):
    '''
    Removes sentences having both positive and negative markers between the objects
    '''
    for s in sentences:
        posA = s.find(objA.name)
        posB = s.find(objB.name)
        pos_one = min(posA, posB)
        pos_two = max(posA, posB)
        for marker in constants.POSITIVE_MARKERS:
 '''           
        

def remove_wrong_marker_positions(sentences, objA, objB):
    '''
    Removes sentences in which no marker is between the objects from a list of sentences.

    sentences:  list
                a list of sentences
    '''
    for s in sentences:
        posA = s.find(objA.name)
        posB = s.find(objB.name)
        pos_first = min(posA, posB)
        pos_second = max(posA, posB)
        no_marker_found = True
        for marker in constants.MARKERS:
            pos_marker = s.find(marker)
            if pos_marker > pos_first and pos_marker < pos_second:
                no_marker_found = False
                break
        if no_marker_found:
            sentences.remove(s)
    return sentences
