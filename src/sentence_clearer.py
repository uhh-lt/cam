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

def remove_double_markers(sentences, objA, objB):
    '''
    Removes sentences having both positive and negative markers between the objects
    '''
    for s in sentences:
        posA = s.find(objA.name)
        posB = s.find(objB.name)
        first_pos = min(posA, posB)
        second_pos = max(posA, posB)
        for m in constants.POSITIVE_MARKERS:
            mPos = s.find(m) 
            for n in constants.NEGATIVE_MARKERS:
                nPos = s.find(n)
                if first_pos < mPos < nPos < second_pos or first_pos < nPos < mPos < second_pos:
                    sentences.remove(s)
    return sentences




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
